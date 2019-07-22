import time

from gpiozero import LED

far_led = LED(21)
med_led = LED(20)
near_led = LED(16)

def light_leds(led_number):
    """Light only the correct LED for the range band"""
    if led_number == 0:
        far_led.on()
        med_led.off()
        near_led.off()
    elif led_number == 1:
        far_led.off()
        med_led.on()
        near_led.off()
    else:
        far_led.off()
        med_led.off()
        near_led.on()

while True:
    for i in range(3):
        light_leds(i)
        time.sleep(0.5)

