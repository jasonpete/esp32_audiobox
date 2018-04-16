# wireless.py
import network
import utime

SSID = "YOUR WIFI SSID"
PASSWORD = "YOUR WIFI PASSWORD"

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)

    start = utime.time()
    while not wlan.isconnected():
        utime.sleep(1)
        if utime.time()-start > 5:
            print("connect timeout!")
            break

    if wlan.isconnected():
        utime.sleep(3)
        print('network config:', wlan.ifconfig())

do_connect()

