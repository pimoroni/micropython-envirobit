#this example takes a reading of the amount of red visible to the colour sensor

import envirolight
import microbit

#flash lights twice, read on third flash
while True:
    envirolight.colour.set_leds(1)
    microbit.sleep(300)
    envirolight.colour.set_leds(0)
    microbit.sleep(300)
    envirolight.colour.set_leds(1)
    microbit.sleep(300)
    envirolight.colour.set_leds(0)
    microbit.sleep(300)
    envirolight.colour.set_leds(1)
    microbit.sleep(300)
    reading = envirolight.colour.rgb()
    microbit.display.scroll(str(reading))
    envirolight.colour.set_leds(0)
    microbit.sleep(3000)
    
