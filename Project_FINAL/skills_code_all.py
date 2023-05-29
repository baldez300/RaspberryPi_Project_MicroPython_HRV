from time import sleep
from machine import Pin, I2C, ADC
from fifo import Fifo
from piotimer import Piotimer
from led import Led

import ssd1306
import network
import ujson
import utime
import time
import socket
import math
import urequests as requests

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

start_btn = Pin(7, Pin.IN, Pin.PULL_UP)
stats_btn = Pin(8, Pin.IN, Pin.PULL_UP)
graph_btn = Pin(9, Pin.IN, Pin.PULL_UP)

ssid = '<your wifi name here>'
password = '<your password here>'

def mean_RR(test_set):
    return sum(test_set) / len(test_set)

def mean_BPM(RR):
    return 60000 / RR

def SDNN(RR, test_set):
    deviations = []
    for x in test_set:
        deviations.append((x - RR)**2)
    sdnn = math.sqrt(sum(deviations) / (len(test_set) - 1))
    return sdnn

def RMSSD(RR, test_set):
    deviations = []
    for i in range(len(test_set) - 1):
        deviations.append(test_set[i+1] - test_set[i])
    dev_list = []
    for deviation in deviations:
        dev_list.append(deviation**2)
    rmssd = math.sqrt(sum(dev_list) - len(deviations))
    return rmssd

class isr_adc:
    def __init__(self, adc_pin_nr):
        self.av = ADC(adc_pin_nr)
        self.samples = Fifo(250)
        self.avrg_fifo = Fifo(10)
        self.avrg_window = 10
        self.old_samples = []
        self.last_y = 0
        self.min = None
        self.max = 0
        self.count_started = False
        self.peak_reached = False
        self.sample_count = 0
        self.old_sample = 0
        self.pns = 1
        self.sns = 1
        
    def handler(self, tid):
        self.samples.put(self.av.read_u16())
        
    def get_stats(self):
        PPI = self.sample_count * 4
        ia.old_samples.append(PPI)
        hr_ = mean_BPM(PPI)
        if len(ia.old_samples) > 2:
            sdnn_ = SDNN(PPI, self.old_samples)
            rmssd_ = RMSSD(PPI, self.old_samples)
        else:
            sdnn_ = 1
            rmssd_ = 1
        self.sample_count = 0
        self.count_started = False
        print(ia.old_samples)
        self.peak_reached = False
        return hr_, sdnn_, rmssd_
        
    def signal_state(self, sample):
        if sample - self.old_sample > 0:
            return 'rising'
        if sample - self.old_sample < 0:
            return 'falling'
        
    def display_stats(self, HR, SDNN, RMSSD):
        display.fill(0)
        display.text(f'BPM:{round(HR)}', 8, 0, 1)
        display.text(f'SDNN: {round(SDNN, 2)}', 8, 10, 1)
        display.text(f'RNSSD: {round(RMSSD, 2)}', 8, 20, 1)
        display.text(f'SNS: {round(ia.sns, 2)}', 8, 30, 1)
        display.text(f'PNS: {round(ia.pns, 2)}', 8, 40, 1)
        display.show()
        
    def display_graph(self, value):
        next_x = 1
        min_val = 31488.14
        max_val = 35848.0
        scale = 63/(max_val - min_val)
        y = int((value - min_val) * scale)
        display.pixel(next_x, y, 1)
        display.show()
        display.scroll(1, 0)
        
ia = isr_adc(26)
tmr = Piotimer(mode = Piotimer.PERIODIC, freq=250, callback = ia.handler)

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    count = 1
    
    while wlan.isconnected() == False:
        display.fill(0)
        display.text('Waiting for', 0, 0)
        display.text('connection...', 0, 10)
        for i in range(count):
            display.fill_rect(1, 30, int(count) * 5, 3, 1)
        display.show()
        count += 1
        sleep(0.1)
        if count >= 25:
            display.fill_rect(1, 13, 0, 3, 40)
            count = 1
            
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    display.fill(0)
    display.text('Connected on', 0, 0)
    display.text(str(ip), 0, 10)
    display.show()
    return ip

connect()
APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"
response = requests.post(
    url = TOKEN_URL,
    data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
    headers = {'Content-Type':'application/x-www-form-urlencoded'},
    auth = (CLIENT_ID, CLIENT_SECRET))

response = response.json() #Parse JSON response into a python dictionary
access_token = response["access_token"] #Parse access token out of the response dictionary
        
display_state = 0
while True:
    run = False
    display.fill(0)
    display.text('SW 2:', 0, 5)
    display.text('Start/stop', 40, 0)
    display.text('measuring', 40, 10)
    display.hline(0, 20, 128, 1)
    display.text('SW 1:', 0, 25 )
    display.text('Show stats', 40, 25)
    display.hline(0, 35, 128, 1)
    display.text('SW 0:', 0, 45)
    display.text('Show graph', 40, 45)
    display.hline(0, 55, 128, 1)
    display.show()
    
    if not start_btn.value():
        run = True
        print(run)
        sleep(1)
    while run:
        if not ia.samples.empty():
            sample = ia.samples.get()
            ia.avrg_fifo.put(sample)
            avrg = round(sum(ia.avrg_fifo.data) / ia.avrg_window)
            ia.avrg_fifo.get()
            
            if avrg > ia.max:
                ia.max = avrg
            if ia.min == None or ia.min > avrg:
                ia.min = avrg
            threshold = (ia.max + ia.min) / 2 + (ia.max -ia.min) * 0.3
            
            if avrg > threshold and ia.signal_state(avrg) == 'rising':
                if not ia.count_started:
                    ia.count_started = True
                if ia.count_started and ia.peak_reached:
                    stats_list = ia.get_stats()
                    if 30 < stats_list[0] < 240:
                        print('BPM:', round(stats_list[0]))
                        if len(ia.old_samples) == 20:
                            dataset = {
                                        "type": "RRI",
                                        "analysis": {"type": "readiness"},
                                        "data": ia.old_samples
                                        }
                            response = requests.post(url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
                                                     headers = { "Authorization": "Bearer {}".format(access_token),
                                                                 "X-Api-Key": APIKEY },
                                                     json = dataset)
                            response = response.json()
                            ia.sns = response["analysis"]["sns_index"]
                            ia.pns = response["analysis"]["pns_index"]
                            ia.old_samples.clear()
                        elif display_state == 0:
                            ia.display_stats(stats_list[0], stats_list[1], stats_list[2])
                    else:
                        print('Invalid BPM value')
            if avrg < threshold and ia.signal_state(avrg) == 'falling' and ia.count_started and not ia.peak_reached:
                ia.peak_reached = True
            if ia.count_started:
                ia.sample_count += 1
                ia.old_sample = avrg
            if ia.sample_count > 750:
                ia.count_started = False
                ia.peak_reached = False
                ia.sample_count = 0
                ia.old_samples = []
                ia.max = 0
                ia.min = None
            if display_state == 1:
                ia.display_graph(sample)
            if not graph_btn.value():
                display_state = 1
                display.fill(0)
                print(display_state)
                sleep(1)
            if not stats_btn.value():
                display_state = 0
                print(display_state)
                sleep(1)
            if not start_btn.value():
                run = False
                print(run)
                sleep(1)
                
        
        
        
        
        
        
