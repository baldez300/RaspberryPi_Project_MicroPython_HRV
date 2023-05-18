# EXERCISE_1

# Task 3 (BONUS)
# Write a similar code as in Task 2, but now turn the LEDs ON and OFF smoothly. 
# (Tip: Study MicroPython’s documentation and search for PWM)

# To turn the LEDs on and off smoothly, we need to use Pulse Width Modulation (PWM) 
from machine import Pin, PWM
import time

# Define LED pins
LED1 = Pin("GP22", Pin.OUT)
LED2 = Pin("GP21", Pin.OUT)
LED3 = Pin("GP20", Pin.OUT)

# Define onboard LED pin
onboard_LED = Pin(25, Pin.OUT)

# Define binary values for each LED combination
values = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]

# Initialize PWM signals for each LED pin
led1_pwm = PWM(LED1)
led2_pwm = PWM(LED2)
led3_pwm = PWM(LED3)

# Set the PWM frequency to 100 Hz
led1_pwm.freq(100)
led2_pwm.freq(100)
led3_pwm.freq(100)

# Set the PWM duty cycle to 0 (LEDs off)
led1_pwm.duty_u16(0)
led2_pwm.duty_u16(0)
led3_pwm.duty_u16(0)

# Loop through the values and display them on the LEDs
while True:
    for value in values:
        # Set the PWM duty cycle for each LED pin to smoothly turn the LED on
        led1_pwm.duty_u16(0xFFFF * value[0])
        led2_pwm.duty_u16(0xFFFF * value[1])
        led3_pwm.duty_u16(0xFFFF * value[2])

        # Blink the onboard LED
        onboard_LED.toggle()

        time.sleep(1)  # Wait for 1 second

        # Set the PWM duty cycle for each LED pin to smoothly turn the LED off
        led1_pwm.duty_u16(0xFFFF * (1 - value[0]))
        led2_pwm.duty_u16(0xFFFF * (1 - value[1]))
        led3_pwm.duty_u16(0xFFFF * (1 - value[2]))

        # Blink the onboard LED
        onboard_LED.toggle()

        time.sleep(1)  # Wait for 1 second
       
