import paho.mqtt.client as paho, os
import urllib.parse as urlparse
import keyboard
import time

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
presTopic = topic + 'pressure'

mqttc.username_pw_set('wioomzqz', "E7AFAC-lUlUB")
mqttc.connect('m20.cloudmqtt.com', 10889)

mqttc.subscribe(presTopic, 0)
mqttc.publish(presTopic, 'Pressure published')

# Continue the loop; exit if an error occurs
rc = 0
message = ''

while (rc == 0):   
    rc = mqttc.loop(.2)
    
print("rc: " + str(rc))

# Disconnect the broker
mqttc.disconnect()
print("Bye!")

