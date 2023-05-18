#EXERCISE_4

from machine import Pin, PWM, I2C
import ssd1306
import utime

# define pins for the rotary encoder
encoderA = Pin(10, Pin.IN, Pin.PULL_UP)
encoderB = Pin(11, Pin.IN, Pin.PULL_UP)
encoderButton = Pin(12, Pin.IN, Pin.PULL_UP)

# define pins for the LEDs
leds = [PWM(Pin(22)), PWM(Pin(21)), PWM(Pin(20))]

# initialize the OLED display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# initialize variables for LED selection and brightness control
selectedLed = 1
brightness = [0, 0, 0]
adjusted = [False, False, False]
encoderAPrev, encoderBPrev = encoderA.value(), encoderB.value()
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
        selectedLed = (selectedLed % 3) + 1
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
            brightness[selectedLed-1] = max(0, min(brightness[selectedLed-1], 100))
            adjusted[selectedLed-1] = True
            leds[selectedLed-1].duty_u16(int(brightness[selectedLed-1] * 100.35))
            updateDisplay()
        encoderAPrev, encoderBPrev, encoderChanged = encoderA.value(), encoderB.value(), False

# initialize the OLED display with the initial values
updateDisplay()

# main loop
while True:
    handleEncoder()
    utime.sleep_ms(10)
