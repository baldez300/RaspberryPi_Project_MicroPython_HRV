# EXERCISE_1

# Task 2
# Write a code that shows the numbers from 0 to 7 in binary format using the three protoboard’s LEDs. 
# LED1 is the least significant bit and LED3 is the most significant bit.
# Change the LED’s values every second.

# At the same blink the Raspberry Pi Pico’s onboard LED every time when the protoboard’s LED values change.

from machine import Pin
import time

# Define LED pins
LED1 = Pin("GP22", Pin.OUT)
LED2 = Pin("GP21", Pin.OUT)
LED3 = Pin("GP20", Pin.OUT)

# Define onboard LED pin
onboard_LED = Pin(25, Pin.OUT)

# Define binary values for each LED combination
values = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]

# Loop through the values and display them on the LEDs
while True:
    for value in values:
        # Display the binary value on the LEDs
        LED1.value(value[0])
        LED2.value(value[1])
        LED3.value(value[2])
        
        # Blink the onboard LED
        onboard_LED.toggle()
        
        time.sleep(1)  # Wait for 1 second
