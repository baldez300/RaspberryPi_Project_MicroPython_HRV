# EXERCISE_5

# Task 2

# Write a code that calculates the basic HRV analysis parameters and shows the values on the OLED:
# ▪ Mean PPI
# ▪ mean heart rate (HR)
# ▪ Standard deviation of PPI (SDNN)
# ▪ Root mean square of successive differences (RMSSD)

# For testing purposes use the following PPI values (given in ms): 
# -Test set 1
# ▪ [1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100]

# The results for the test set 1 should be
# ▪ mean PPI = 1050 ms 
# ▪ MeanHR= 57bpm 
# ▪sdnn= 52ms
# ▪ rmssd = 100 ms

# -Test set 2
# ▪ [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]

# The results for the test set 2 should be
# • mean PPI = 805 ms 
# • MeanHR=75bpm 
# • sdnn=31ms
# • rmssd=43ms

# I used the "Encoder Button" to toggle between ("Test Set 1" and "Test Set 2") results.

from machine import Pin, I2C
import ssd1306
import time
import math

# OLED Display setup
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Encoder Button setup
button = machine.Pin(12, Pin.IN, Pin.PULL_UP)

# PPI values for Test set 1 and Test set 2
ppi_test_set_1 = [1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100]
ppi_test_set_2 = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]

# Define labels for the test sets
test_set_1_label = "Test Set 1"
test_set_2_label = "Test Set 2"

# Function to calculate HRV analysis parameters
def calculate_hrv_params(ppi):
    mean_ppi = sum(ppi) / len(ppi)
    mean_hr = 60 / mean_ppi * 1000
    sdnn = math.sqrt(sum((x - mean_ppi) ** 2 for x in ppi) / len(ppi))
    rmssd = math.sqrt(sum((ppi[i+1] - ppi[i]) ** 2 for i in range(len(ppi)-1)) / (len(ppi)-1))
    return mean_ppi, mean_hr, sdnn, rmssd

# Initial test set to display
test_set = ppi_test_set_1
test_set_label = test_set_1_label

while True:
    # Check if button is pressed
    if not button.value():
        # Switch to the other test set
        if test_set == ppi_test_set_1:
            test_set = ppi_test_set_2
            test_set_label = test_set_2_label
        else:
            test_set = ppi_test_set_1
            test_set_label = test_set_1_label
        time.sleep(0.2)  # debounce
        
    # Calculate HRV analysis parameters
    mean_ppi, mean_hr, sdnn, rmssd = calculate_hrv_params(test_set)
    
    # Print parameters on OLED display
    oled.fill(0)
    oled.text(test_set_label, 0, 0)
    oled.text("Mean PPI: {} ms".format(round(mean_ppi)), 0, 20)
    oled.text("Mean HR: {} bpm".format(round(mean_hr)), 0, 30)
    oled.text("SDNN: {} ms".format(round(sdnn)), 0, 40)
    oled.text("RMSSD: {} ms".format(round(rmssd)), 0, 50)
    oled.show()
    
    time.sleep(0.1)  # update every 100 ms
