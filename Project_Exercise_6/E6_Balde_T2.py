# EXERCISE_6

# Task 2:
# For this exercise you will make a request to Kubios cloud to get a sample heart rate analysis. 
# You will need to make a POST request to authenticate with Kubios and create a session. 
# Kubios will return a session key to you in the POST response with a dataset to configure your analysis parameters. 
# You are provided with code to do everything except connecting to WiFi, creating the dataset, and printing out your results (SNS index and PNS index) to the OLED. 
# In order to create the dataset it is helpful to understand python dictionaries. 
# 5. Data Structures — Python 3.11.3 documentation

# import urequests as requests
# import ujson
# APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a" CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
# CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
# LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login" TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token" REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"
# response = requests.post(
# url = TOKEN_URL,
# data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID), headers = {'Content-Type':'application/x-www-form-urlencoded'},
# auth = (CLIENT_ID, CLIENT_SECRET))

# response = response.json() #Parse JSON response into a python dictionary
# access_token = response["access_token"] #Parse access token out of the response dictionary
# intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800] #Interval data to be sent to KuniosCloud
# Form data set as instructed in

# https://analysis.kubioscloud.com/v2/portal/documentation/api_analytics.html#analyze-a-dataset-v2
# TODO Create your dataset here
# The dataset that you send will be a python dictionary that is made up of two "Key": "Pairs" and one nested dictionary
# The dataset will need a key value pair for "type" which describes the type of data that we are sending. In this case we are sending RR intervals so we can set type as "RRI"
# EXERCISE_6
# The aim:
# The aim is to learn to use the Raspberry Pi Pico W to make HTTP requests to a server and handle the responses from those servers.

# The second key pair is to send the actual "data", and there we can send out intervals array, provided above
# The final part is for the "analysis" analysis will have a nested dictionary key pair value to describe the type of analysis that we wish to be done
# The key here is "type" (again) and the value will be "readiness" to describe the type of analysis that we want.
# The analysis member can be quite a bit more complex, but for our needs, the readiness is more than enough
# dataset creation HERE
# Make the readiness analysis with the given data

# response = requests.post(
# url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
# headers = { "Authorization": "Bearer {}".format(access_token), #use access token to access your KubiosCloud analysis session
# "X-Api-Key": APIKEY },
# json = data_set) #dataset will be automatically converted to JSON by the urequests library
# response = response.json()
# Print out the SNS and PNS values on the OLED screen

import urequests as requests
import ujson
import utime
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import network
import machine


ssid = 'Aaa'
password = 'Bbb12345'

Oled_scl = 15
Oled_sda = 14
i2c = I2C(1, scl=Pin(Oled_scl), sda=Pin(Oled_sda), freq=400000)
Oled_width = 128
Oled_height = 64
oled = SSD1306_I2C(Oled_width, Oled_height, i2c)
oled.fill(0)
oled.show()

def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    count = 1
    while wlan.isconnected() == False:
        oled.fill(0)
        oled.text('Waiting for', 0, 0)
        oled.text('connection...', 0, 10)
        oled.show()
        for i in range(count):
            oled.rect(0, 30, Oled_width - 1, 5, 1)
            oled.fill_rect(1, 30, int(count) * 5, 3, 1)
        count += 1
        machine.idle()
        if count >= 25:
            oled.fill_rect(1, 13, 0, 3, 40)
            count = 1
    ip = wlan.ifconfig()[0]
    return ip

connect()

APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
response = requests.post(
    url=TOKEN_URL,
    data='grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
    headers={'Content-Type':'application/x-www-form-urlencoded'},
    auth=(CLIENT_ID, CLIENT_SECRET))

response = response.json()
access_token = response["access_token"]
intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]
dataset = {
    "type": "RRI",
    "analysis": {"type": "readiness"},
    "data": intervals
}

response = requests.post(
    url="https://analysis.kubioscloud.com/v2/analytics/analyze",
    headers={"Authorization": "Bearer {}".format(access_token), "X-Api-Key": APIKEY},
    json=dataset)

response = response.json()
print(response)
sns = response["analysis"]["sns_index"]
pns = response["analysis"]["pns_index"]

while True:
    try:
        oled.fill(0)
        oled.text('SNS: %s' %str(sns), 0, 0)
        oled.text('PNS: %s' %str(pns), 0, 20)
        oled.show()
    except KeyboardInterrupt:
        machine.reset()
