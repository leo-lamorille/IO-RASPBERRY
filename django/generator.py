#!/usr/bin/python3
from random import randint
from datetime import datetime

class Sensor:
    def __init__(_self, mac, name, interval):
        _self.mac = mac
        _self.name = name
        _self.interval = interval
    
    def __str__(_self):
        return "('{mac}', '{name}', {interval})".format(mac = _self.mac, name=_self.name, interval=_self.interval)
    
    @staticmethod
    def columns():
        return "dashboard_sensor(macAddress, name, `interval`)"

class Data:
    def __init__(_self, tStamp, humidity, temperature, airQuality, sensor_id):
        _self.tStamp = tStamp
        _self.humidity = humidity
        _self.temperature = temperature
        _self.airQuality = airQuality
        _self.sensor_id = sensor_id
        
    def __str__(_self):
        return "({tStamp}, {humidity}, {temperature}, {airQuality}, '{sensor_id}')".format(
            tStamp = _self.tStamp, 
            humidity = _self.humidity, 
            temperature=_self.temperature, 
            airQuality=_self.airQuality, 
            sensor_id=_self.sensor_id)
    
    @staticmethod  
    def columns():
        return "dashboard_datas(tStamp, humidity, temperature, airQuality, sensor_id)"

NOW = int(datetime.now().timestamp())
TIMELAPSE= 200 * 86400 # 10 * 86400 = 10 days
OUTPUT="generated-values.sql"

print("Generating from {} to {}".format(datetime.fromtimestamp(NOW - TIMELAPSE), datetime.fromtimestamp(NOW)))
sensors = [Sensor('24:6F:28:24:6B:50', 'Cécile En Cieux', randint(5, 100)), 
            Sensor('24:6F:28:24:6B:52', 'Gérard Manvussa', randint(5, 100)),
            Sensor('24:6F:28:24:6B:54', 'Tom Égérie', randint(5, 100)),
            Sensor('24:6F:28:24:6B:55', 'Yves Atrovite', randint(5, 100)),
            Sensor('24:6F:28:24:6B:56', 'Yvon Enbavé', randint(5, 100))]

datas = []

SENSOR_BUFFER = "INSERT INTO {} VALUES ".format(Sensor.columns())
DATAS_BUFFER = ""


cpt_sensor = 0
cpt_data = 0
for sensor in sensors:
    print("{}/{} sensors done".format(cpt_sensor, len(sensors)))
    cpt_sensor += 1
    SENSOR_BUFFER += "\n\t{},".format(str(sensor))
    last_humidity = 50
    last_temperature = 20 ## -20 ==> 50
    last_air_quality = 2000 # 1500 - 2500
    for timestamp in range(NOW - TIMELAPSE, NOW, sensor.interval):
        if cpt_data % 3000 == 0:
            DATAS_BUFFER = DATAS_BUFFER[:-1] + ";\n\nINSERT INTO {} VALUES ".format(Data.columns())
        humidity = max(min(last_humidity + randint(-15, 15), 100), 0)
        temperature = max(min(last_temperature + randint(-5, 5), 55), -20)
        airQuality = max(min(last_air_quality + randint(-20, 20), 2600), 1400)
        new_data = Data(timestamp, humidity, temperature, airQuality, sensor.mac)
        DATAS_BUFFER += "{},".format(str(new_data))
        cpt_data += 1
        
        
print("{len}/{len} sensors done".format(len=len(sensors)))        

with open(OUTPUT, 'w') as output_file:
    output_file.write(SENSOR_BUFFER[:-1]+';\n')
    output_file.write(DATAS_BUFFER[:-1]+';\n')


print("Generation ended, see {}".format(OUTPUT))