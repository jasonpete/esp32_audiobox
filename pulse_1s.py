from machine import Pin
import utime

switch1 = Pin(25,Pin.OUT,value = 0)
switch2 = Pin(26,Pin.OUT,value = 0)

while True:
    switch1.value(1)
    switch2.value(1)
    utime.sleep_ms(500)
    switch1.value(0)
    switch2.value(0)
    utime.sleep_ms(500)
