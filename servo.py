# import board
# import busio
# import adafruit_pca9685
# i2c = busio.I2C(board.SCL, board.SDA)
# hat = adafruit_pca9685.PCA9685(i2c)
# 
# 
# hat.frequency = 60
# led_channel = hat.channels[0]
# 
# # Increase brightness:
# for i in range(0, 0xffff, 50):
#     led_channel.duty_cycle = i
#          
# # Decrease brightness:
# for i in range(0xffff, 0, -50):
#     led_channel.duty_cycle = i
# 

import time
import datetime
from gpiozero import DistanceSensor, LED

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

for theta in range(0, 180):
    kit.servo[4].angle = theta
    print(theta)
    time.sleep(0.02)
time.sleep(0.5)
for theta in range(180, 0, -1):
    kit.servo[4].angle = theta
    print(theta)
    time.sleep(0.02)

