#!/usr/bin/python

# Lab 2 - Sending SNS and SQS Data
# Make sure your host and region are correct.

import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time

#Setup our MQTT client and security certificates
#Make sure your certificate names match what you downloaded from AWS IoT

mqttc = AWSIoTMQTTClient("1234")

#Make sure you use the correct region!
mqttc.configureEndpoint("data.iot.ap-southeast-1.amazonaws.com",8883)
mqttc.configureCredentials("../AmazonRootCA1.pem","../ratchet.private.key","../ratchet.cert.pem")

#Function to encode a payload into JSON
def json_encode(string):
        return json.dumps(string)

mqttc.json_encode=json_encode

#Declaring our variables
message ={
  'Critical': 1,
  'AlertMessage': "Temperature exceeded",
  'AlertCount': 4,
  'Device': "RAT Internals"
}

#Encoding into JSON
message = mqttc.json_encode(message)

#This sends our test message to the iot topic
def send():
    mqttc.publish("iot", message, 0)
    print ("Message Published")


#Connect to the gateway
mqttc.connect()
print "Connected"

#Loop until terminated
while True:
    send()
    time.sleep(5)

mqttc.disconnect()
#To check and see if your message was published to the message broker go to the MQTT Client and subscribe to the iot topic and you should see your JSON Payload