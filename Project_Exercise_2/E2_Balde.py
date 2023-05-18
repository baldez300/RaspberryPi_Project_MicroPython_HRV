# EXERCISE_2

# Write a program that reads the state of all four protoboard buttons and uses the state to control protoboard’s LEDs. 
# Use polling to read the protoboard buttons SW0, SW1 and SW2 state and use interrupt for the rotary encoder push button (ROT_Push).

# Program should work as follows:

# SW0, SW1 and SW2 are used to toggle LEDs (LED1 LED2 and LED3 ) on and off.
# Each button controls one LED. When a button is pressed the state of the controlled LED is toggled.
# Each press should be counted only once; pressing and holding the button may not cause the LED to blink.
# Rotary encoder’s button (ROT_Push) presses should be detected by using an interrupt.
# When the rotary encoder’s button is pressed all LEDs are switched off.

# Import necessary libraries
from machine import Pin, I2C
import ssd1306
import time
from ssd1306 import SSD1306_I2C

# Set up the OLED display
WIDTH = 128
HEIGHT = 64
ID_value = 1

# Define the pins
SW0_PIN = 'GP9'
SW1_PIN = 'GP8'
SW2_PIN = 'GP7'
ROT_PUSH_PIN = 'GP12'
LED1_PIN = 'GP22'
LED2_PIN = 'GP21'
LED3_PIN = 'GP20'

# Initialize OLED screen
i2c = I2C(ID_value, scl=Pin('GP15'), sda=Pin('GP14'), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Initialize GPIO pins
sw0 = Pin(SW0_PIN, Pin.IN, Pin.PULL_UP)
sw1 = Pin(SW1_PIN, Pin.IN, Pin.PULL_UP)
sw2 = Pin(SW2_PIN, Pin.IN, Pin.PULL_UP)
rot_push = Pin(ROT_PUSH_PIN, Pin.IN, Pin.PULL_UP)
led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)
led3 = Pin(LED3_PIN, Pin.OUT)

# Define variables to keep track of LED states
led1_state = False
led2_state = False
led3_state = False

# Define functions to toggle LED states
def toggle_led1():
    global led1_state
    led1_state = not led1_state
    led1.value(led1_state)

def toggle_led2():
    global led2_state
    led2_state = not led2_state
    led2.value(led2_state)

def toggle_led3():
    global led3_state
    led3_state = not led3_state
    led3.value(led3_state)

# Define function to update OLED screen with LED states
def update_screen():
    oled.fill(0)
    oled.text("LED1 = " + ("On" if led1_state else "Off"), 0, 0)
    oled.text("LED2 = " + ("On" if led2_state else "Off"), 0, 10)
    oled.text("LED3 = " + ("On" if led3_state else "Off"), 0, 20)
    oled.show()

# Initialize LED states and OLED screen
led1.value(led1_state)
led2.value(led2_state)
led3.value(led3_state)
update_screen()

# Define function to handle rotary encoder button presses
def rot_push_pressed(p):
    global led1_state, led2_state, led3_state
    led1_state = False
    led2_state = False
    led3_state = False
    led1.value(led1_state)
    led2.value(led2_state)
    led3.value(led3_state)
    update_screen()

# Attach interrupt handler for rotary encoder button
rot_push.irq(trigger=Pin.IRQ_FALLING, handler=rot_push_pressed)

# Poll buttons and toggle LEDs accordingly
while True:
    if not sw0.value():
        toggle_led1()
        update_screen()
        while not sw0.value():
            time.sleep(0.1)
            pass
    if not sw1.value():
        toggle_led2()
        update_screen()
        while not sw1.value():
            time.sleep(0.1)
            pass
    if not sw2.value():
        toggle_led3()
        update_screen()
        while not sw2.value():
            time.sleep(0.1)
            pass

