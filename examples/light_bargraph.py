# bargraph code modified from Simon Monk's code
# in Microbit for Mad Scientists
# Go buy his book, it's great

import tcs3472
import microbit

tcs3472 = tcs3472.tcs3472()

def light_level():
    max_level = 0
    for i in range(0, 10):
        light_level = tcs3472.brightness() / 100
        if light_level > max_level:
            max_level = light_level
    return max_level

def bargraph(a):
    microbit.display.clear()
    for y in range (0, 5):
        if a > y:
            for x in range (0, 5):
                microbit.display.set_pixel(x, 4-y, 9)

while True:
    bargraph(light_level())
    microbit.sleep(10)
