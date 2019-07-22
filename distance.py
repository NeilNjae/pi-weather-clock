
import time
from enum import Enum

from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=17, trigger=4)

class RangeBand(Enum):
    FAR = 1
    MEDIUM = 2
    NEAR = 3

def find_range_band():
    """Calculate the range band, as measured by the ultrasonic sensor"""
    print(ultrasonic.distance)
    if ultrasonic.distance > 0.8:
        return RangeBand.FAR
    elif ultrasonic.distance > 0.4:
        return RangeBand.MEDIUM
    else:
        return RangeBand.NEAR

while True:
    range_band = find_range_band()
    print(ultrasonic.distance, range_band)
    time.sleep(0.2)

