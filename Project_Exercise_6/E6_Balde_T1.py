# EXERCISE_6

# Task1:
# Connect your PC and your Pico to your group’s WiFi access point in the classroom. Identify the IP address on your PC. 
# Navigate to your project directory on your computer and start the python webserver that you use to copy files to your Pico when you use mpremote. 
# This will start a local webserver on your computer that will serve your files to you.

# Using the urequests python module, you will make a simple get request to the python server located at http://<your_PC_IP>:8000


import urequests as requests

url = "http://192.168.161.18:8000/"

response = requests.get(url)

print(response.text)

response.close()
