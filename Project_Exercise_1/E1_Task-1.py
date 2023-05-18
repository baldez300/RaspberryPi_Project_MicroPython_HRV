# EXERCISE_1

# Task 1
# Write a code that turns the protoboard’s LEDs ON and OFF in sequence.
# Switch the values every second.

from machine import Pin
import time

# Define LED pins
LED1 = Pin("GP22", Pin.OUT)
LED2 = Pin("GP21", Pin.OUT)
LED3 = Pin("GP20", Pin.OUT)

# Define the sequence
sequence = [LED1, LED2, LED3]

# Loop through the sequence and switch the values every second
while True:
    for led in sequence:
        led.value(not led.value())  # Toggle the LED on/off
        time.sleep(1)  # Wait for 1 second
