import math, random, time
from gmaps.directions import Directions
from gmaps.errors import NoResults, RateLimitExceeded
import pprint

with open('google-api-key.txt', 'r') as f:
    API_KEY = f.read().strip()

FROM = 'london'

d = Directions(api_key=API_KEY)

def random_lat_lon():
    x, y, z = [random.gauss(0, 1) for i in xrange(3)]
    n = math.sqrt(x**2 + y**2 + z**2)
    x, y, z = x/n, y/n, z/n

    lat = math.acos(y)
    lon = math.atan2(x, z)
    return lat * 180 / math.pi - 90, lon * 180 / math.pi


def get_steps(lat, lon):
    try:
        res = d.directions(FROM, (lat, lon))
    except NoResults:
        return None
    except RateLimitExceeded:
        print 'exhausted, sleeping for a bit'
        time.sleep(10)
        return None

    assert len(res) == 1
    assert len(res[0]['legs']) == 1

    leg = res[0]['legs'][0]

    steps = []
    total_duration = 0
    for step in leg['steps']:
        total_duration += step['duration']['value']
        steps.append((step['end_location']['lat'], step['end_location']['lng'], total_duration))

    # distance = res[0]['legs'][0]['distance']['value']
    # duration = res[0]['legs'][0]['duration']['value']
    # return duration

    return steps

while True:
    lat, lon = random_lat_lon()
    # lat, lon = 59.3294, 18.0686
    print lat, lon
    steps = get_steps(lat, lon)

    if steps is not None:
        print steps
        f = open('log-gmaps.txt', 'a')
        for lat, lon, duration in steps:
            print >>f, lat, lon, duration
        f.close()
