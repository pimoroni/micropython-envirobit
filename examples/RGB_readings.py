# this example takes a reading of the amount of red, green and blue visible to the colour sensor
# displays the result as three numbers on the microbit screen, eg (120, 88, 30)
# remember to copy the tcs3472 library onto the microbit before flashing this code

import tcs3472
import microbit

tcs3472 = tcs3472.tcs3472()

#flash lights twice, read on third flash
while True:
    tcs3472.set_leds(1)
    microbit.sleep(300)
    tcs3472.set_leds(0)
    microbit.sleep(300)
    tcs3472.set_leds(1)
    microbit.sleep(300)
    tcs3472.set_leds(0)
    microbit.sleep(300)
    tcs3472.set_leds(1)
    microbit.sleep(300)
    reading = tcs3472.rgb()
    microbit.display.scroll(str(reading))
    tcs3472.set_leds(0)
    microbit.sleep(3000)
    
