# EXECISE_3 
# This task is divided into two parts that can be completed separately and then integrated into a complete solution.

# Part 1. Implement a program that uses Piotimer and ADC to sample PPG signal at 250Hz frequency
# and passes the sampled data to the main program. In the first phase main program can just print each sample so that you can,
# for example with the data with Thonny’s plotter view.

# Part 2. Implement an algorithm that finds the heart rate from sampled PPG signal.
# The program should work with the sensor when it is returned to OMA.

from machine import I2C, Pin
import ssd1306
from piotimer import Piotimer
from machine import ADC
from fifo import Fifo
import utime

# initialize the ADC pin for reading PPG signal
adc = ADC(26)

# define the sample buffer 
samples = Fifo(100)
sample_list = []
average_window = 10
average_fifo = Fifo(average_window)

# Piotimer event handler for reading PPG samples at 250Hz rate
def read_sample(tid):
    samples.put(adc.read_u16())

# start the Piotimer with the specified sampling period
tim = Piotimer(mode=Piotimer.PERIODIC, freq=250, callback=read_sample)
utime.sleep(1)

# initialize variables for heart rate calculation
last_peak = None
last_trough = None
hrv_list = []

# initialize the OLED screen
i2c = I2C(1, scl=Pin('GP15'), sda=Pin('GP14'))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# main loop to calculate heart rate
while True:
    if not samples.empty():
        # Get one value from interrupt fifo
        value = samples.get()
        average_fifo.put(value)
        average = int(sum(average_fifo.data)/average_window)
        average_fifo.get()
       
        # append the sample to the list
        sample_list.append(average)
        
        # check if we have enough samples to calculate heart rate
        if len(sample_list) >= 750:
            avg_line =sum(sample_list)*1.1/len(sample_list)
            
   
            # identify the peaks in the signal
            peaks = []
            intervals = []
            for i in range(1, len(sample_list)-1):
                if sample_list[i] > sample_list[i-1] and sample_list[i] > sample_list[i+1] and sample_list[i] > avg_line:
                    peaks.append(i)
            
            # calculate the time difference between two consecutive peaks
            if len(peaks) >= 2:
                
                for k in range(len(peaks)-1):
                    time = (peaks[k+1] - peaks[k]) / 250  # time difference in seconds
                    intervals.append(time)
                time_diff = sum(intervals)/len(intervals)
                
                hr = int(60 / time_diff)
                print("Heart rate: {} bpm".format(hr))
                # clear OLED screen
                oled.fill(0)
                # print heart rate on OLED screen
                oled.text("HR: {} bpm".format(hr), 0, 0)
                oled.show()

            sample_list.clear()            
    utime.sleep_ms(1)
