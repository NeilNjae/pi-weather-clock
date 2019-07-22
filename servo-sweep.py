
import time

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

