#coding: utf-8

import microbit
import gc
import struct

ADDR=0x76

# 500ms standby time, 16 filter coef
CONFIG = 0b10010000

# x16 oversampling, normal mode
CTRL_MEAS = 0b10110111

# x16 humidity oversampling
CTRL_HUM = 0b00000101

R_CHIPID = 0xD0
R_VERSION = 0xD1
R_SOFTRESET = 0xE0
R_CONTROL = 0xF4
R_HCONTROL = 0xF2
R_CONFIG  = 0xF5
R_STATUS = 0xF3

def i2c_read(address, reg, length=1):
    microbit.i2c.write(address, bytes([reg]), repeat=True)
    return microbit.i2c.read(address, length)
    
def i2c_write(address, reg, value):
    microbit.i2c.write(address, bytes([reg, value]))

class bme280():
    def __init__(self, i2c_bus=None, addr=ADDR):
        self._temperature = 0
        self._pressure = 0
        self._altitude = 0
        self._qnh = 1013.25 # hPa

        self.addr = addr

        i2c_write(self.addr, R_SOFTRESET, 0xB6)
        microbit.sleep(200)
        i2c_write(self.addr, R_HCONTROL, CTRL_HUM)
        microbit.sleep(200)
        i2c_write(self.addr, R_CONTROL, CTRL_MEAS)
        microbit.sleep(200)
        i2c_write(self.addr, R_CONFIG, CONFIG)
        microbit.sleep(200)

        self.compensation = i2c_read(self.addr, 0x88, 26)
        self.compensation += i2c_read(self.addr, 0xe1, 7)

    def set_qnh(self, qnh):
        self._qnh = qnh

    def temperature(self):
        self.update()
        gc.collect()
        return self._temperature

    def pressure(self):
        self.update()
        gc.collect()
        return self._pressure
        
    def humidity(self):
        self.update()
        gc.collect()
        return self._humidity

    def altitude(self):
        self.update()
        gc.collect()
        return self._altitude
        
    def all(self):
        self.update()
        gc.collect()
        return self._temperature, self._pressure, self._humidity, self._altitude

    def update(self):
        dig_T1, dig_T2, dig_T3, \
            dig_P1, dig_P2, dig_P3, \
            dig_P4, dig_P5, dig_P6, \
            dig_P7, dig_P8, dig_P9, \
            _, \
            dig_H1, dig_H2, dig_H3, \
            reg_E4, reg_E5, reg_E6, \
            dig_H6 = struct.unpack("<HhhHhhhhhhhhbBhBbBbb", self.compensation)

        dig_H4 = (reg_E5 & 0x0f) | (reg_E4 << 4)
        dig_H5 = (reg_E5 >> 4) | (reg_E6 << 4)

        if dig_H4 & (1 << 12):
            dig_H4 -= 1 << 12
        if dig_H5 & (1 << 11):
            dig_H5 -= 1 << 12
            
        raw = i2c_read(self.addr, 0xF7, 8)

        raw_temp=(raw[3]<<12)|(raw[4]<<4)|(raw[5]>>4)
        raw_press=(raw[0]<<12)|(raw[1]<<4)|(raw[2]>>4)
        raw_hum=(raw[6]<<8)|raw[7]

        var1=(raw_temp/16384.0-dig_T1/1024.0)*dig_T2
        var2=(raw_temp/131072.0-dig_T1/8192.0)*(raw_temp/131072.0-dig_T1/8192.0)*dig_T3
        temp=(var1+var2)/5120.0
        t_fine=(var1+var2)

        var1=t_fine/2.0-64000.0
        var2=var1*var1*dig_P6/32768.0
        var2=var2+var1*dig_P5*2
        var2=var2/4.0+dig_P4*65536.0
        var1=(dig_P3*var1*var1/524288.0+dig_P2*var1)/524288.0
        var1=(1.0+var1/32768.0)*dig_P1
        press=1048576.0-raw_press
        press=(press-var2/4096.0)*6250.0/var1
        var1=dig_P9*press*press/2147483648.0
        var2=press*dig_P8/32768.0
        press=press+(var1+var2+dig_P7)/16.0

        var1 = t_fine - 76800.0
        var2 = dig_H4 * 64.0 + (dig_H5 / 16384.0) * var1
        var3 = raw_hum - var2
        var4 = dig_H2 / 65536.0
        var5 = 1.0 + (dig_H3 / 67108864.0) * var1
        var6 = 1.0 + (dig_H6 / 67108864.0) * var1 * var5
        var6 = var3 * var4 * (var5 * var6)

        h = var6 * (1.0 - dig_H1 * var6 / 524288.0)
        h = max(0, min(100, h))

        self._temperature = temp
        self._pressure = press / 100.0
        self._humidity = h
        self._altitude = 44330.0 * (1.0 - pow(self._pressure / self._qnh, (1.0/5.255)))

bmp280 = bme280
        
if __name__ == "__main__":
    b = bme280()
    while True:
        t, p, h, a = b.all()
        print("T: {t}, P: {p}, H: {h}, A: {a}".format(t=t,p=p,h=h,a=a))
        microbit.sleep(1000)
