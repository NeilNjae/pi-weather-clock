import requests
from bs4 import BeautifulSoup


WEATHER_LOCATIONS = {
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


# 3-day forecast for Milton Keynes
response = requests.get('https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/2642465')
# print('Response code', response.status_code)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'xml')
    # print(soup.prettify())
    forecasts = []
    for item in soup.find_all('item'):
        # print(item.title.string)
        item_dict = {}
        summary_pair = item.title.string.split(',')[0]
        summary = summary_pair.split(':')[1].strip()
        item_dict['Summary'] = summary
        for term in item.description.string.split(','):
            term_parts = term.split(':', maxsplit=1)
            item_dict[term_parts[0].strip()] = term_parts[1].strip()
        # item_dict = {term.split(':', maxsplit=1)[0].strip(): term.split(':', maxsplit=1)[1].strip() 
        #   for term in item.description.string.split(',')}
        # item_dict['Summary'] = item.title.string.split(',')[0].split(':')[1].strip()
        forecasts.append(item_dict)
        # print(item_dict)
    print(forecasts)

    for forecast in forecasts:
        print("{} at position {}".format(forecast['Summary'], WEATHER_LOCATIONS[forecast['Summary']]))

