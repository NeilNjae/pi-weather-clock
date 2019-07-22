import time
import datetime
from gpiozero import DistanceSensor, LED

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

while True:
    stheta = input('enter index:')
    theta = int((int(stheta) - 1) * 180 / 11 )
    kit.servo[4].angle = 180 - theta

