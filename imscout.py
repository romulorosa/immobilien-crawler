# -*- coding: utf-8 -*-

import asyncio
import json
import math
import re
from collections import namedtuple
from decimal import Decimal

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from datetime import datetime

from texttable import Texttable


class ScoreCalculator:

    FORMULAS = {
        'space': lambda x, y, z: 50*x + 2.5*y + 1.4*z-datetime.now().year,
        'price': lambda x: math.pow(1200/x, 1.2) * 100,
        'places': lambda x: 100 * pow(x, 1.2),
    }


class Immobile:
    GOOGLE_MAPS_API_KEY = ''
    GOOGLE_PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&key={}'  # noqa

    def __init__(self, data: json, score_calculator: ScoreCalculator):
        general_data = data.get('general_data')
        geo_data = data.get('geo_data')

        # GENERAL DATA
        self._id = int(general_data.get('obj_scoutId'))
        self._region_1 = general_data.get('obj_regio1')
        self._region_2 = general_data.get('obj_regio2')
        self._region_3 = general_data.get('obj_regio3')
        self._street = general_data.get('obj_street')
        self._heating_type = general_data.get('central_heating')
        self._total_rent = Decimal(general_data.get('obj_totalRent') or '0.0')
        self._base_rent = Decimal(general_data.get('obj_baseRent'))
        self._year_construction = int(general_data.get('obj_yearConstructed') or 1920)
        self._living_space = float(general_data.get('obj_livingSpace'))
        self._zipcode = general_data.get('obj_zipCode')
        self._condition = general_data.get('obj_condition')
        self._pets_allowed = general_data.get('obj_petsAllowed')
        self._internet_down_speed = general_data.get('obj_telekomDownloadSpeed')
        self._has_kitchen = general_data.get('obj_hasKitchen')
        self._has_garden = general_data.get('obj_hasGarden')
        self._no_rooms = float(general_data.get('obj_noRooms') or -1)
        self._no_subways = 0
        self._no_trains = 0
        self._no_supermarkets = 0

        # SCORE
        self._score = 0
        self._score_calculator = score_calculator

        # GEO DATA
        self._lat = geo_data.lat
        self._lng = geo_data.lng

    def __repr__(self):
        return '<Immobile: ID={} Score={} Price={} Size={}² Pos=({}, {}) Address={} {} {}>'.format(
            self._id,
            round(self._score, 2),
            self._total_rent,
            self._living_space,
            self._lat,
            self._lng,
            self._street,
            self._region_1,
            self._region_2
        )

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

    @staticmethod
    async def __fetch_url(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def __google_places(self):
        async with ClientSession() as session:
            json_supermarkets = await self.__fetch_url(session, self.__places_supermarket_url)
            json_trains = await self.__fetch_url(session, self.__places_train_station_url)
            json_subways = await self.__fetch_url(session, self.__places_subway_station_url)

            self._no_supermarkets = len(json.loads(json_supermarkets).get('results'))
            self._no_trains = len(json.loads(json_trains).get('results'))
            self._no_subways = len(json.loads(json_subways).get('results'))

            return self._no_supermarkets, self._no_trains, self._no_subways

    @property
    def score(self):
        return self._score

    @property
    def address(self):
        return '{} {} {}'.format(self._street, self._region_1, self._region_2)

    def calculate_score(self):
        score = 0
        for name, formula in self._score_calculator.FORMULAS.items():
            method_name = '_calculate_{}'.format(name)
            method = getattr(self, '_calculate_{}'.format(name))
            if not method:
                raise ValueError('You mus implement the method {}'.format(method_name))
            score += method(formula)

        self._score = score

        return score

    def _calculate_space(self, formula):
        return formula(self._no_rooms, self._living_space, self._year_construction)

    def _calculate_price(self, formula):
        return formula(self._total_rent or Decimal('1.3') * self._base_rent)

    def _calculate_places(self, formula):
        if not self.GOOGLE_MAPS_API_KEY:
            return 0

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.__google_places())

        return sum([formula(x) for x in response])

    @property
    def __places_supermarket_url(self):
        # location = {}, {} & radius = {} & type = {} & key = {}
        return self.GOOGLE_PLACES_URL.format(
            self._lat, self._lng, 800, 'supermarket', self.GOOGLE_MAPS_API_KEY
        )

    @property
    def __places_train_station_url(self):
        return self.GOOGLE_PLACES_URL.format(
            self._lat, self._lng, 1000, 'train_station', self.GOOGLE_MAPS_API_KEY
        )

    @property
    def __places_subway_station_url(self):
        return self.GOOGLE_PLACES_URL.format(
            self._lat, self._lng, 1000, 'subway_station', self.GOOGLE_MAPS_API_KEY
        )

    def listfy(self):
        return [
            self._id,
            self._score,
            self.address,
            self._total_rent,
            self._base_rent,
            self._year_construction,
            self._living_space,
            self._no_rooms,
            self._condition,
            self._no_trains,
            self._no_subways,
            self._no_supermarkets,
        ]


class ImmobilienScoutCrawler:

    def __init__(self, urls):
        if not urls:
            raise ValueError('You must specify urls to be fetched')
        self._urls = urls

    @staticmethod
    async def _fetch_url(session: ClientSession, url: str):
        async with session.get(url, timeout=60*60) as response:
            return await response.text()

    async def _fetch_all_urls(self, session: ClientSession,):
        results = await asyncio.gather(
            *[self._fetch_url(session, url) for url in self._urls],
            return_exceptions=True
        )
        return results

    async def _fire_requests(self):
        async with ClientSession() as session:
            htmls = await self._fetch_all_urls(session)
            return dict(zip(self._urls, htmls))

    def get_htmls(self):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self._fire_requests())
        return response

    def parse_htmls(self, htmls):
        parsed_htmls = []
        GeoData = namedtuple('GeoData', 'lat lng')
        geo_data = None

        for html in htmls.values():
            parsed = BeautifulSoup(html)
            all_scripts = parsed.find_all('script')
            parsed_geo_data = [
                scrp.get_text() for scrp in all_scripts if 'getMapOptions' in scrp.get_text()
            ]
            if parsed_geo_data:
                parsed_geo_data = parsed_geo_data[0]
                lat_rx = re.compile('lat=(\d+.?\d+)')
                lng_rx = re.compile('lon=(\d+.?\d+)')
                lat = lat_rx.findall(parsed_geo_data)[0]
                lng = lng_rx.findall(parsed_geo_data)[0]
                geo_data = GeoData(lat, lng)

            general_data = parsed.find('script').get_text()
            immobilie_data = json.loads(general_data.split('keyValues = ', 1)[-1].split(';\n')[0])

            parsed_htmls.append({'general_data': immobilie_data, 'geo_data': geo_data})

        return parsed_htmls

    def run(self):
        htmls = self.get_htmls()
        parsed = self.parse_htmls(htmls)
        immobilies = [Immobile(d, ScoreCalculator()) for d in parsed]
        for imo in immobilies:
            imo.calculate_score()

        immobilies = sorted(immobilies, reverse=True)

        txtTable = Texttable(max_width=240)
        txtTable.set_cols_dtype(['i', 'f', 't', 'f', 'f', 'i', 'f', 'i', 't', 'i', 'i', 'i'])
        txtTable.add_row([
            'Id', 'Score', 'Address', 'Total rent (€)', 'Base rent (€)', 'Constructed',
            'Living Space', 'Rooms', 'Condition', 'Train Stations', 'Subway Stations',
            'Supermarkets'
        ])

        for imo in immobilies:
            txtTable.add_row(imo.listfy())
        print(txtTable.draw())
