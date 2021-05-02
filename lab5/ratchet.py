#!/usr/bin/python

# Lab 5 - Device Shadows
# Make sure your host and region are correct.

import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient, AWSIoTMQTTClient
import json
import time
from random import randint

# Our motor is not currently running.
MOTOR_STATUS = "OFF"

#Setup our MQTT client and security certificates
#Make sure your certificate names match what you downloaded from AWS IoT

#Note we will use the Shadow Client here, rather than the regular AWSIoTMQTTClient.
mqttShadowClient = AWSIoTMQTTShadowClient("ratchet")

#Make sure you use the correct region!
mqttShadowClient.configureEndpoint("data.iot.ap-southeast-1.amazonaws.com",8883)
mqttShadowClient.configureCredentials("../AmazonRootCA1.pem","../xxxxxxxxxx-private.pem.key","../xxxxxxxxxx-certificate.pem.crt")

#Set up the Shadow handlers
shadowClient=mqttShadowClient.createShadowHandlerWithName("ratchet",True)

#We can retrieve the underlying MQTT connection from the Shadow client to make regular MQTT publish/subscribe
mqttClient = mqttShadowClient.getMQTTConnection()

def updateDeviceShadow():
    global shadowClient
    #Set the shadow with the current motor status and check if it was successful by calling the custom callback
    print "Updating shadow with reported motor status"
    shadowMessage = {"state":{"reported":{"MOTOR": MOTOR_STATUS}}}
    shadowMessage = json.dumps(shadowMessage)
    shadowClient.shadowUpdate(shadowMessage, customShadowCallback_Update, 5)

# Custom Shadow callback for updating, checks if the update was successful.
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        print "Motor status successfully updated in Device Shadow"
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")
        
#Function to encode a payload into JSON
def json_encode(string):
        return json.dumps(string)

mqttClient.json_encode=json_encode

#This sends a random temperature message to the topic, 
#value and the correct unit of measurement.
def send():
    global MOTOR_STATUS
    temp = randint(0, 100)
    message ={
        'temp': temp,
        'unit' : 'F'
    }
    message = mqttClient.json_encode(message)
    mqttClient.publish("data/temperature", message, 0)
    print "Temperature Message Published"

#Connect to the gateway
mqttShadowClient.connect()
print "Connected"

#Set the initial motor status in the device shadow
updateDeviceShadow()

#Loop until terminated
while True:
    send()
    time.sleep(5)

mqttShadowClient.disconnect()

#To check and see if your message was published to the message broker go to the MQTT Client and subscribe to the iot topic and you should see your JSON Payload
