import paho.mqtt.client as paho, os
import urllib.parse as urlparse
import time
from sense_hat import SenseHat
import json


# Define event callbacks
def on_connect(mqttc, obj, flags, rc):
    print("flags, rc: " + str(flags) + " " + str(rc))

def on_message(mqttc, obj, msg):
    print("Recieved message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, msg_id):
    print("msg_id: " + str(msg_id))

def on_subscribe(mqttc, obj, msg_id, granted_qos):
    print("Subscribed: " + str(msg_id) + " " + str(granted_qos))

def on_log(mqttc, obj, level, log_string):
    print(log_string)

#Create a client instance
mqttc = paho.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://m20.cloudmqtt.com')
url = urlparse.urlparse(url_str)
topic = 'jonashoft/'
tempTopic = topic + 'temperature'
humTopic = topic + 'humidity'
presTopic = topic + 'pressure'

#mqttc.username_pw_set('wioomzqz', "E7AFAC-lUlUB")
mqttc.connect('192.168.0.81', 8000)

mqttc.subscribe(topic, 0)
mqttc.publish(topic, 'Getting started ...')

# Continue the loop; exit if an error occurs
rc = 0
message = ''
sense = SenseHat()
while (1):   
    mqttc.loop(timeout=1)
    time.sleep(10)

    mqttc.publish(tempTopic, json.dumps({"temperature" : sense.temperature,"timestamp":time.time()}))

    mqttc.publish(humTopic, json.dumps({"humidity" : sense.humidity,"timestamp":time.time()}))

    mqttc.publish(presTopic, json.dumps({"pressure" : sense.pressure,"timestamp":time.time()}))
    
    
print("rc: " + str(rc))

# Disconnect the broker
mqttc.disconnect()
print("Bye!")

