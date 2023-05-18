# EXERCISE_5
# The aim:
# Individual work, expected 5-10 hours including lectures.
# The aim is to learn to connect the Pico W to local WiFi network and to calculate basic HRV analysis parameters.

# Task 1:
# Write code that connects your protoboard to ICT laboratory’s WiFi network and displays the IP address on the OLED.

import network
import socket
from time import sleep
import machine
import ssd1306
from machine import Pin, I2C

ssid = 'Aaa'
password = 'Bbb12345'

def connect(oled):
    #Clear the OLED display
    oled.fill(0)
    
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    
    # Display IP address on OLED
    oled.text("IP Address:", 0, 0)
    oled.text(ip, 0, 20)
    oled.show()

try:
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    connect(oled)
except KeyboardInterrupt:
    machine.reset()
