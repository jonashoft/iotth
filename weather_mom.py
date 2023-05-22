from flask import Flask, request
import paho.mqtt.client as paho, os
from pymongo import MongoClient
import datetime
import json


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
        self.mqttc.subscribe(humTopic, 0)
        self.mqttc.subscribe(presTopic, 0)
    

    def on_connect(self,mqttc, obj, flags, rc):
        print("flags, rc: " + str(flags) + " " + str(rc))

    def on_message(self,mqttc, obj, msg):
        collection = msg.topic.split('/')[-1] 
        document = json.loads(msg.payload)
        db[collection].insert_one(document) 
        #self.temperature.append(msg.payload)
        #print(document)
        

    def on_subscribe(self,mqttc, obj, msg_id, granted_qos):
        print("Subscribed: " + str(msg_id) + " " + str(granted_qos))


mqtt = MQTTClient('192.168.0.81', 8000)

mongo_client =  MongoClient("localhost", 27017)
db = mongo_client.WeatherStation

def create__date_query(date):
    if date:
        datetimeObj = datetime.datetime.strptime(date, "%Y-%m-%d")
        timestamp = datetime.datetime.timestamp(datetimeObj)
        query = {"$and" : [{"timestamp" : {"$gte" : timestamp}},{"timestamp" : {"$lt" : timestamp+(24*60*60)}}]}
    else:
        query = {}

    return query

app = Flask(__name__)

@app.route('/weather')
def index():
    temp_dates = list(set([datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d") for x in list(db.temperature.distinct("timestamp"))]))
    pres_dates = list(set([datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d") for x in list(db.pressure.distinct("timestamp"))]))
    hum_dates = list(set([datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d") for x in list(db.humidity.distinct("timestamp"))]))
    return {"temperature" : temp_dates, "pressure" : pres_dates, "humidity" : hum_dates}

@app.route('/weather/temperature')
def temperature():
    date = request.args.get("date")
    query = create__date_query(date)
    cursor = db.temperature.find(query,{'_id': False})
    list_cur = list(cursor)
    json_data = json.dumps(list_cur)
    
    return json_data
    #return str(mqtt.temperature[-1])

@app.route('/weather/humidity')
def humidity():
    date = request.args.get("date")
    query = create__date_query(date)
    cursor = db.humidity.find(query,{'_id': False})
    list_cur = list(cursor)
    json_data = json.dumps(list_cur)
    
    return json_data

@app.route('/weather/pressure')
def pressure():
    date = request.args.get("date")
    query = create__date_query(date)
    cursor = db.pressure.find(query,{'_id': False})
    list_cur = list(cursor)
    json_data = json.dumps(list_cur)

    return json_data

if __name__ == '__main__':
    

    #mqttc.username_pw_set('wioomzqz', "E7AFAC-lUlUB")
    
    app.run(debug=True, port=5000, host='192.168.0.81')