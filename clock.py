import requests
from bs4 import BeautifulSoup

import time
import datetime
from enum import Enum


from gpiozero import DistanceSensor, LED

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
servo = kit.servo[4]
servo_position = 1

ultrasonic = DistanceSensor(echo=17, trigger=4)
far_led = LED(21)
med_led = LED(20)
near_led = LED(16)

class RangeBand(Enum):
    FAR = 1
    MEDIUM = 2
    NEAR = 3

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

def get_forecast():
    """Read the forecasts from the BBC"""
    forecasts = []
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
    return forecasts


def find_range_band():
    """Calculate the range band, as measured by the ultrasonic sensor"""
    if ultrasonic.distance > 0.8:
        return RangeBand.FAR
    elif ultrasonic.distance > 0.4:
        return RangeBand.MEDIUM
    else:
        return RangeBand.NEAR


def summary_of_range(forecasts, range_band):
    if forecasts:
        if range_band == RangeBand.FAR:
            return forecasts[0]['Summary']
        elif range_band == RangeBand.MEDIUM:
            return forecasts[1]['Summary']
        else:
            return forecasts[2]['Summary']
    else:
        return 'Sunny'

def light_leds(range_band):
    """Light only the correct LED for the range band"""
    if range_band == RangeBand.FAR:
        far_led.on()
        med_led.off()
        near_led.off()
    elif range_band == RangeBand.MEDIUM:
        far_led.off()
        med_led.on()
        near_led.off()
    else:
        far_led.off()
        med_led.off()
        near_led.on()


def servo_target_position(summary):
    """Give the servo angle for this weather"""
    return int(WEATHER_POSITIONS[summary] * 180  / 12)


def move_servo(angle):
    global servo_position
    
    if angle > servo_position:
        step = 1
    else:
        step = -1

    for i in range(servo_position, angle, step):
        servo.angle = i
        time.sleep(0.02)

    servo_position = angle


forecasts = get_forecast()
print(forecasts)

while True:
    range_band = find_range_band()
    summary = summary_of_range(forecasts, range_band)
    # print(range_band, summary)
    light_leds(range_band)
    servo_target = servo_target_position(summary)
    move_servo(servo_target)
    time.sleep(0.2)


# print(forecasts)
#     
#         for forecast in forecasts:
#             print("{} at position {}".format(forecast['Summary'], WEATHER_LOCATIONS[forecast['Summary']]))
#     
# while True:
#     #     print(datetime.datetime.utcnow(), ultrasonic.distance)
#     if ultrasonic.distance > 0.8:
#         far_led.on()
#         med_led.off()
#         near_led.off()
#     elif ultrasonic.distance > 0.4:
#         far_led.off()
#         med_led.on()
#         near_led.off()
#     else:
#         far_led.off()
#         med_led.off()
#         near_led.on()
# 
