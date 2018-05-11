from microbit import i2c, sleep, pin8
import struct

ADDR = 0x29

class tcs3472:
    def __init__(self):
        i2c.write(ADDR, b'\x80\x03')
        i2c.write(ADDR, b'\x81\x2b')

    def scaled(self):
        crgb = self.raw()
        if crgb[0] > 0:
            return tuple(float(x) / crgb[0] for x in crgb[1:])

        return (0,0,0)

    def rgb(self):
        return tuple(int(x * 255) for x in self.scaled())

    def light(self):
        return self.raw()[0]

    def valid(self):
        i2c.write(ADDR, b'\x93')
        return i2c.read(ADDR, 1)[0] & 1

    def raw(self):
        i2c.write(ADDR, b'\xb4')
        return struct.unpack("<HHHH", i2c.read(ADDR, 8))
        
    def set_leds(self, state):
        pin8.write_digital(state)
        
if __name__ == "__main__":
    t = tcs3472()
    while True:
        t.set_leds(1)
        sleep(200)
        r, g, b = t.rgb()
        l = t.light()
        t.set_leds(0)
        print("#{:02x}{:02x}{:02x} - {}".format(r, g, b, l))
        sleep(300)
