#EXERCISE_4
# Write a program that implements a menu system to control LED brightness.
# The menu has two modes: LED selection and brightness control. User toggles between the modes by pressing the encoder button.

# When the program is in LED selection mode turning the encoder switches between LEDs.
# The selected LED is displayed on the screen.

# When user presses the button program enters brightness control mode where turning the encoder adjusts the brightness of the selected LED.

# The current brightness is displayed on the screen as both percentage (0 – 100%) and a horizontal bar.

# Turning the knob immediately increases or decreases the brightness of the LED and updates the display.

# When user presses the button to switch back to LED selection mode the current brightness will remain on the LED.
# Adjusting one LEDs brightness may not affect the other LEDs.

from machine import Pin, PWM, I2C
import ssd1306
import utime

# define pins for the rotary encoder
encoderA = Pin(10, Pin.IN, Pin.PULL_UP)
encoderB = Pin(11, Pin.IN, Pin.PULL_UP)
encoderButton = Pin(12, Pin.IN, Pin.PULL_UP)

# define pins for the LEDs
led1 = PWM(Pin(22))
led2 = PWM(Pin(21))
led3 = PWM(Pin(20))

# initialize the OLED display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# initialize variables for LED selection and brightness control
selectedLed = 1
brightness = [0, 0, 0]
adjusted = [False, False, False]
encoderAPrev = encoderA.value()
encoderBPrev = encoderB.value()
encoderChanged = False

# function to update the OLED display with the selected LED and brightness
def updateDisplay():
    oled.fill(0)
    oled.text("LED " + str(selectedLed), 0, 0)
    oled.rect(0, 20, 128, 10, 1)
    if adjusted[selectedLed-1]:
        oled.fill_rect(0, 20, int(brightness[selectedLed-1] * 1.28), 10, 1)
    else:
        oled.fill_rect(0, 20, 0, 10, 1)
    oled.text(str(brightness[selectedLed-1]) + "%", 0, 40)
    oled.show()

# function to handle rotary encoder input
def handleEncoder():
    global selectedLed, brightness, encoderAPrev, encoderBPrev, encoderChanged
    if encoderButton.value() == 0:
        # button pressed, switch modes
        if selectedLed == 1:
            selectedLed = 2
        elif selectedLed == 2:
            selectedLed = 3
        else:
            selectedLed = 1
        updateDisplay()
        while encoderButton.value() == 0:
            pass
    else:
        # knob turned, adjust brightness
        if encoderA.value() != encoderAPrev or encoderB.value() != encoderBPrev:
            encoderChanged = True
        if encoderChanged:
            if encoderA.value() != encoderBPrev:
                brightness[selectedLed-1] += 1
            elif encoderB.value() != encoderAPrev:
                brightness[selectedLed-1] -= 1
            if brightness[selectedLed-1] < 0:
                brightness[selectedLed-1] = 0
            elif brightness[selectedLed-1] > 100:
                brightness[selectedLed-1] = 100
            if not adjusted[selectedLed-1]:
                adjusted[selectedLed-1] = True
            if selectedLed == 1:
                led1.duty_u16(int(brightness[0] * 100.35)) # 655.35 
            elif selectedLed == 2:
                led2.duty_u16(int(brightness[1] * 100.35))
            else:
                led3.duty_u16(int(brightness[2] * 100.35))
            updateDisplay()
        encoderAPrev = encoderA.value()
        encoderBPrev = encoderB.value()
        encoderChanged = False

# initialize the OLED display with the initial values
updateDisplay()

# main loop
while True:
    handleEncoder()
    utime.sleep_ms(10)
