# immobilien-crawler
This is a simple crawler to create a score ranking of immobilier 

## About
This script was used as a exercise to learn a lit bit more about `asyncio` lib. 
It has a simple crawler which know how to parse pages from https://www.immobilienscout24.de and also creates a ranking
based on a very rudimentar score calculator (tunned for my necessities).

The script try to combine information from immobilienscout24 and alson Google Places. The score is based on simple metrics, such as living space, number of rooms, rent, etc (from immobilienscout24), supermarkets, train station and subway stations (from Google Places).

For be able to retrieve informations from Google Places, you might want to get in the development platform for creating an API KEY.

## How to use it
If you want to run this script as it is, you just need to get the URLS from your search at https://www.immobilienscout24.de and put them in a array. Here is one example:

```
crawler = ImmobilienScoutCrawler([
    'https://www.immobilienscout24.de/expose/110448261/',
    'https://www.immobilienscout24.de/expose/110794529/',
])

htmls = crawler.get_htmls()
parsed = crawler.parse_htmls(htmls)
immobilies = [Immobile(d, ScoreCalculator()) for d in parsed]
for imo in immobilies:
    imo.calculate_score()

immobilies = sorted(immobilies, reverse=True)

txtTable = Texttable(max_width=240)
txtTable.set_cols_dtype(['i', 'f', 't', 'f', 'f', 'i', 'f', 'i', 't', 'i', 'i', 'i'])
txtTable.add_row([
    'Id', 'Score', 'Address', 'Total rent (€)', 'Base rent (€)', 'Constructed',
    'Living Space', 'Rooms', 'Condition', 'Train Stations', 'Subway Stations', 'Supermarkets'
])

for imo in immobilies:
    txtTable.add_row(imo.listfy())
print(txtTable.draw())
```

## How to tune metrics

You can adjust the metrics used to create the rank as you wish. Everything that you need is make some adjustments on class `ScoreCalculator` or event create your own one. If you want to add some new metrics in the class (not only adjust the formula already created) you will need to implement a new method on class `Immobile` following the given pattern:
```
def _calculate_<your_metric_name>():
    pass
```

Let's suppose that you want to add a metric called `distance_from_job`. So the code should be something like this:
```
class ScoreCalculator:

    FORMULAS = {
        'space': lambda x, y, z: 50*x + 2.5*y + 1.4*z-datetime.now().year,
        'price': lambda x: math.pow(1200/x, 1.2) * 100,
        'places': lambda x: 100 * pow(x, 1.2),
        'distance_from_job': lambda x: x * x
    }

class Immobile:
    GOOGLE_MAPS_API_KEY = ''
    GOOGLE_PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&key={}'  # noqa
    [...]

    def _calculate_distance_from_job(self, formula):
        pass
```

### Output example
