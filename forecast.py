import requests
from bs4 import BeautifulSoup

import time
import datetime


WEATHER_POSITIONS = {
    'Sunny': 1,
    'Clear': 1,
    'Partly Cloudy': 2,
    'White Cloud': 3,
    'Sunny Intervals': 2,
    'Black Cloud': 4,
    'Light Rain Showers': 5,
    'Light Rain': 6,
    'Heavy Rain': 7,
    'Heavy Rain Showers': 5,
    'Light Snow': 11,
    'Light Snow Showers': 11,
    'Heavy Snow': 12,
    'Heavy Snow Showers': 12,
    'Sleet': 9,
    'Sleet Showers': 9,
    'Hail': 10,
    'Hail Showers': 10,
    'Thunder': 8,
    'Thundery Showers': 8,
    'Mist': 12,
    'Fog': 12
    }

# Location code for Milton Keynes
LOCATION = '2642465'

def get_forecast(location):
    """Read the forecasts from the BBC"""

     # default value if we can't read the forecast
    forecasts = [{'Summary': 'Sunny'} * 3]
    
    # 3-day forecast for Milton Keynes
    response = requests.get('https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/{}'.format(location))
    
    if response.status_code == 200: # success
    
        soup = BeautifulSoup(response.content, 'xml')
        forecasts = []
        for item in soup.find_all('item'):
            item_dict = {}
            # summary looks like "Tonight: Light Rain, Minimum Temperature: 12⁰C (53⁰F)"
            # split it on the comma to get the "Tonight: Light Rain" part...
            summary_pair = item.title.string.split(',')[0]
            # ... then split that on the colon to get the "Light Rain"
            summary = summary_pair.split(':')[1].strip()
            item_dict['Summary'] = summary
            # The description text is a series of terms, separated by commas
            for term in item.description.string.split(','):
                # each term is a title and value, separated by a colon
                term_parts = term.split(':', maxsplit=1)
                item_dict[term_parts[0].strip()] = term_parts[1].strip()
            forecasts.append(item_dict)
            # print(item_dict)
    return forecasts


forecasts = get_forecast(LOCATION)
last_location_refresh = datetime.datetime.now(datetime.timezone.utc)
print(forecasts)

while True:
    for i in range(3):
        summary = forecasts[i]['Summary']
        print(i, summary, WEATHER_POSITIONS[summary])
        time.sleep(0.5)

    if (datetime.datetime.now(datetime.timezone.utc) - last_location_refresh).total_seconds() > 10:
        forecasts = get_forecast(LOCATION)
        last_location_refresh = datetime.datetime.now(datetime.timezone.utc)
        print(forecasts)
