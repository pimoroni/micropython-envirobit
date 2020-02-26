from microbit import sleep
import tcs3472

light_sensor = tcs3472.tcs3472() 

while True:
    light_sensor.set_leds(1)
    sleep(1000)
    light_sensor.set_leds(0)
    sleep(1000)
    
