# uses light sensor as a proximity sensor
# darkness (lower than trigger) = surprised face

from microbit import *
import tcs3472

tcs3472 = tcs3472.tcs3472()

# change the trigger - a lower number means you need
# to get closer to trigger the surprised face
trigger = 400

while True:
    light_level = tcs3472.light()
    if light_level < trigger :
        display.show(Image.SURPRISED)
    else:
        display.show(Image.HAPPY)
