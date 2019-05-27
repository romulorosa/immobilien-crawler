# immobilien-crawler


## About
This is a simple crawler to create a score ranking of immobilier.
The script was used as a exercise to learn a lit bit more about `asyncio` lib. 
It has a simple crawler which know how to parse pages from https://www.immobilienscout24.de and also creates a ranking
based on a very rudimentar score calculator (tunned for my necessities).

The script try to combine information from immobilienscout24 and alson Google Places. The score is based on simple metrics, such as living space, number of rooms, rent, etc (from immobilienscout24), supermarkets, train station and subway stations (from Google Places).

For be able to retrieve informations from Google Places, you might want to sing up to development platform for creating an API KEY.

### Output example
### Output example
```bash
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| Id        | Score    | Address                                               | Total rent (€) | Base rent (€) | Constructed | Living Space | Rooms | Condition       | Train Stations | Subway Stations | Supermarkets |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 61675789  | 4856.069 | no_information Hessen Frankfurt_am_Main               | 910.000        | 840.000       | 1955        | 65.000       | 2     | modernized      | 1              | 7               | 15           |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111642648 | 3338.906 | Zum Brommenhof  Hessen Frankfurt_am_Main              | 1190.000       | 1020.000      | 2003        | 56.000       | 2     | mint_condition  | 4              | 1               | 10           |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111646632 | 3050.105 | no_information Hessen Frankfurt_am_Main               | 830.000        | 685.000       | 1910        | 46.000       | 2     | modernized      | 1              | 4               | 9            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111642937 | 2982.590 | no_information Hessen Frankfurt_am_Main               | 915.000        | 790.000       | 1908        | 66.000       | 3     | modernized      | 1              | 0               | 11           |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111655439 | 2887.943 | Kronberger Stra&szlig;e Hessen Frankfurt_am_Main      | 1180.000       | 940.000       | 1955        | 58.000       | 2     | fully_renovated | 1              | 5               | 7            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111555673 | 2623.746 | Pfarrer-Perabo-Platz Hessen Frankfurt_am_Main         | 0.000          | 900.000       | 1995        | 60.000       | 2     | fully_renovated | 1              | 0               | 9            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111288996 | 2582.065 | Pariser Stra&szlig;e Hessen Frankfurt_am_Main         | 1183.000       | 990.000       | 2019        | 52.170       | 2     | first_time_use  | 2              | 0               | 8            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111126026 | 2518.069 | Europa-Allee Hessen Frankfurt_am_Main                 | 1000.000       | 750.000       | 2017        | 38.600       | 1     | mint_condition  | 2              | 0               | 8            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111325118 | 2451.290 | K&ouml;lner Str. Hessen Frankfurt_am_Main             | 866.000        | 666.000       | 2014        | 36.000       | 1     | fully_renovated | 2              | 1               | 7            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111477560 | 2445.416 | M&uuml;hlheimer Stra&szlig;e Hessen Offenbach_am_Main | 0.000          | 900.000       | 2016        | 70.460       | 2     | mint_condition  | 2              | 0               | 7            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 110467290 | 2316.436 | no_information Hessen Frankfurt_am_Main               | 1160.000       | 980.000       | 2018        | 57.000       | 2     | first_time_use  | 1              | 3               | 5            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 110794529 | 2231.756 | Hahnstra&szlig;e Hessen Frankfurt_am_Main             | 865.000        | 695.000       | 2014        | 40.000       | 1     | mint_condition  | 1              | 0               | 7            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 107130643 | 2190.063 | no_information Hessen Frankfurt_am_Main               | 1130.000       | 925.000       | 1920        | 60.000       | 2     | well_kept       | 1              | 5               | 3            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 111179952 | 2117.082 | Westring Hessen Frankfurt_am_Main                     | 1016.920       | 757.370       | 2018        | 72.130       | 3     | no_information  | 0              | 6               | 0            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
| 110670210 | 2106.725 | Lyonerstra&szlig;e Hessen Frankfurt_am_Main           | 1103.000       | 873.000       | 2010        | 67.000       | 2     | mint_condition  | 1              | 0               | 6            |
+-----------+----------+-------------------------------------------------------+----------------+---------------+-------------+--------------+-------+-----------------+----------------+-----------------+--------------+
```



## Setting up the environment

*Cloning the repo*
```bash
mkdir ~/imscout
cd ~/imscout
git clone git@github.com:romulorosa/immobilien-crawler.git
```

### Using python virtual environment

This code was written and tested on Python >= 3.5. Make sure you have at least this version installed on your computer.

*Creating virtualenv*
```bash
virtualenv -p /usr/bin/python3.7 ~/venvs/imscout
source ~/venvs/imscout/bin/activate
```

*Installing Python requirements*
```bash
pip install -r requirements.txt
```

If you want to run this script as it is, you just need to get the URLS from your search at https://www.immobilienscout24.de and put them in a array. Here is one example:

```python
crawler = ImmobilienScoutCrawler([
    'https://www.immobilienscout24.de/expose/110448261/',
    'https://www.immobilienscout24.de/expose/110794529/',
])

crawler.run()
```

You can also input the urls from stdin
```bash
python imscout.py https://www.immobilienscout24.de/expose/111667003 https://www.immobilienscout24.de/expose/111676616
```

### Using Docker

If you are not familiar with Python environments you might want run it through Docker containers.

*The first step is build the image*
```bash
docker build -t immobilien-crawler .
```

*Now you are able to run a container*
```bash
docker run -it --rm immobilien-crawler python imscout.py https://www.immobilienscout24.de/expose/111667003 https://www.immobilienscout24.de/expose/109702102
```

*You either can specify your Google API key as a env var*
```bash
docker run -it --env GOOGLE_MAPS_API_KEY=<your_api_key_here> --rm immobilien-crawler python imscout.py https://www.immobilienscout24.de/expose/111667003 https://www.immobilienscout24.de/expose/109702102
```

## How to tune metrics

You can adjust the metrics used to create the rank as you wish. Everything that you need is make some adjustments on class `ScoreCalculator` or event create your own one. If you want to add some new metrics in the class (not only adjust the formula already created) you will need to implement a new method on class `Immobile` following the given pattern:
```python
def _calculate_<your_metric_name>():
    pass
```

Let's suppose that you want to add a metric called `distance_from_job`. So the code should be something like this:
```python
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
