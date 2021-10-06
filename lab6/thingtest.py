# Lab 6 - LWT
#!/usr/bin/python

import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time

#Setup our MQTT client and security certificates
#Make sure your certificate names match what you downloaded from AWS IoT

#Function to encode a payload into JSON
def json_encode(string):
        return json.dumps(string)

#Creating last will message and encoding
lastWill = "Help I have disconnected"
lastWill = json_encode(lastWill)

mqttc = AWSIoTMQTTClient("1234")

#Make sure you use the correct region!
mqttc.configureEndpoint("data.iot.ap-southeast-1.amazonaws.com",8883)
mqttc.configureCredentials("../AmazonRootCA1.pem","../ratchet.private.key","../ratchet.cert.pem")
mqttc.configureLastWill("lwt", lastWill, 1)


mqttc.connect()
print "Connected"
print "Press Control + C to Crash"

# Loop forever
while True:
        pass

