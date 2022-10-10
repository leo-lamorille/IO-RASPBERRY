import mariadb
import paho.mqtt.client as mqtt
import mysql.connector as database
import time
import json


def getCursor():
    conn = mariadb.connect(
        user="mariadb",
        password="mariadb",
        host="10.5.0.2",
        database="mariadb"

    )
    return conn.cursor()


cursor = getCursor()


def get_client():
    broker_address = "10.5.0.10"
    client = mqtt.Client("Python connector")
    client.connect(broker_address, 1883)
    return client


def on_message(client, userdata, message):
    messageJson = json.loads(message.payload.decode('utf-8'))
    print(messageJson)
    if message.topic == "sensor/register":
        register_sensor(message, messageJson)
    elif message.topic == "sensor/data":
        handle_data(messageJson)


def getSensorData(macAddress):
    try:
        cursor.execute(
            "SELECT * FROM dashboard_sensor WHERE `macAddress`=%s LIMIT 1;", (macAddress,))
        record = cursor.fetchall()
        if len(record) > 0:
            sensor = record[0]
            return sensor
    except database.Error as e:
        print(f"Error retrieving entry (getSensorData) from database: {e}")


def verify_if_sensor_exists(macAddress):
    try:
        cursor.execute(
            "SELECT * FROM dashboard_sensor WHERE `macAddress`=%s LIMIT 1;", (macAddress,))
        record = cursor.fetchall()
        if len(record) > 0:
            return True
        else:
            return False
    except database.Error as e:
        print(f"Error retrieving entry (verify) from database: {e}")


def register_sensor(message, jsonData):
    try:

        sensorExist = verify_if_sensor_exists(jsonData['MacAddress'])
        print(sensorExist)
        if (sensorExist == False):
            statement = "INSERT INTO dashboard_sensor (macAddress,`interval`) VALUES (%s, %d);"
            data = (jsonData['MacAddress'], int(jsonData['delay']))
            print(data)
            cursor.execute(statement, data)
            cursor.connection.commit()

            print("Sensor registered")

        # Get params from database
        print("verification")
        print(jsonData['MacAddress'])
        cursor.execute(
            "SELECT macAddress,`interval` FROM dashboard_sensor WHERE macAddress=%s", (jsonData['MacAddress'],))
        record = cursor.fetchall()
        if len(record) > 0:
            sensor = record[0]
            print(sensor)
            print("sensor/params/"+sensor[0])
            client.publish("sensor/params/"+sensor[0], json.dumps({
                "macAddress": sensor[0],
                "interval": str(sensor[1])
            }))

    except Exception as e:
        print(f"Error verifying sensor: {e}")


def handle_data(jsonData):
    sensor = getSensorData(jsonData['MacAddress'])
    print('handle data')
    print(sensor)
    if sensor is not None:
        try:
            print("Inserting data")
            statement = "INSERT INTO dashboard_datas (sensor_id,tStamp, temperature, humidity, airQuality) VALUES (%s,%d, %d, %d, %d);"
            data = (sensor[0], jsonData['Time'], jsonData['Temperature'],
                    jsonData['Humidity'], jsonData['AirQuality'])
            print(data)
            cursor.execute(statement, data)
            cursor.connection.commit()
        except database.Error as e:
            print(f"Error inserting data into database: {e}")

 #   if verify_if_sensor_exists_by_id(jsonData['id']) != None:
  #      dbname = get_database()
   #     dbname.data.insert_one(json.dumps(jsonData))


client = get_client()

client.on_message = on_message

# client.subscribe("sensor/register")
client.subscribe("sensor/data")
client.subscribe("sensor/register")
client.subscribe("sensor/params/24:6F:28:24:6B:50")
client.loop_forever()
