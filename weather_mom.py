from flask import Flask
import paho.mqtt.client as paho, os





#Create a client instance

class MQTTClient():
    def __init__(self,host,port):
        self.mqttc = paho.Client()
        
        self.temperature = []
        # Assign event callbacks
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe

        # Parse CLOUDMQTT_URL (or fallback to localhost)
        topic = 'jonashoft/'
        tempTopic = topic + 'temperature'
        humTopic = topic + 'humidity'
        presTopic = topic + 'pressure'

        self.mqttc.connect(host,port)
        self.mqttc.loop_start()
        self.mqttc.subscribe(tempTopic, 0)
    

    def on_connect(self,mqttc, obj, flags, rc):
        print("flags, rc: " + str(flags) + " " + str(rc))

    def on_message(self,mqttc, obj, msg):
        print("Recieved message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        self.temperature.append(msg.payload)
        

    def on_subscribe(self,mqttc, obj, msg_id, granted_qos):
        print("Subscribed: " + str(msg_id) + " " + str(granted_qos))


mqtt = MQTTClient('192.168.0.81', 8000)


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hej Verden'

@app.route('/weather/temperature')
def temperature():
    #Do code
    return str(mqtt.temperature[-1])

@app.route('/weather/humidity')
def humidity():
    #Do code
    return 'Humidity is 90%'
if __name__ == '__main__':
    

    #mqttc.username_pw_set('wioomzqz', "E7AFAC-lUlUB")
    
    app.run(debug=True, port=5000, host='192.168.0.81')