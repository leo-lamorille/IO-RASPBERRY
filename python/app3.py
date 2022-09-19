from pymongo import MongoClient
import paho.mqtt.client as mqtt
import time
import json


def get_database():
    CONNECTION_STRING = "mongodb://10.5.0.2"
    client = MongoClient(CONNECTION_STRING)
    return lient['sensor']


def get_client():
    broker_address = "10.5.0.10"
    client = mqtt.Client("P1")
    client.connect(broker_address, 1883)
    return client


def on_message(client, userdata, message):
    print(message.payload.decode('utf-8'))
    messageJson = json.loads(message.payload.decode('utf-8'))
    if message.topic == "sensor/register":
        register_sensor(message, messageJson)
    # elif message.topic == "sensor/data":
    #    handle_data(messageJson)


def verify_if_sensor_exists(macAddress):
    db = get_database()
    return db.sensors.find_one({"macAddress": macAddress})


def register_sensor(message, jsonData):
    dbname = get_database()
    if verify_if_sensor_exists(jsonData['macAddress']) == None:
        dbname.sensors.insert_one(
            {macAddress: messageJson.mac,
             parameters: messageJson.parameters
             })
    dbSensor = db.sensors.find_one({"macAddress": macAddress})
    client.publish("sensor/data/" + dbSensor["macAddress"],
                   {id: dbSensor["_id"], parameters: dbSensor["parameters"]})


def verify_if_sensor_exists_by_id(id):
    db = get_database()
    return db.sensors.find_one({"_id": id})


def handle_data(jsonData):
    print(jsonData)

 #   if verify_if_sensor_exists_by_id(jsonData['id']) != None:
  #      dbname = get_database()
   #     dbname.data.insert_one(json.dumps(jsonData))


def send_message(client):
    jsonObject = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }
    client.publish("sensor/data", json.dumps(jsonObject))


client = get_client()

client.on_message = on_message

# client.subscribe("sensor/register")
client.subscribe("sensor/data")
client.loop_forever()
