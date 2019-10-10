# this example turns the onboard LEDs on and off

from microbit import sleep
import envirolight

c=envirolight.colour()

while True:
    c.set_leds(1)
    sleep(200)
    c.set_leds(0)
    sleep(300)
