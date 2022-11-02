from django.shortcuts import render, redirect
from dashboard.models import sensor, datas
from django.db.models import Avg
from django.http import HttpResponse
from datetime import datetime, timedelta
from time import time
import random


def __replace_query_param(path, name, value) -> str:
    split = path.split('?')
    query = None
    if len(split) == 1:
        return path + '?{name}={value}'.format(name=name, value=value)
    else:
        query = split[1]
    result: str = ""
    params: str = query.split('&')
    added: bool = False
    for param in params:
        param = param.split('=')
        param_name = param[0]
        param_value = param[1]
        if name == param_name:
            param_value = value
            added = True
        result += "&" if result != "" else ""
        result += "{name}={value}".format(name=param_name, value=param_value)
    if not added:
        result += "&" if result != "" else ""
        result += "{name}={value}".format(name=name, value=value)

    return "{path}?{query}".format(path=split[0], query=result)


def __averages_by_timestamps(timestamp_start, timestamp_stop):
    averages = datas.objects.filter(tStamp__range=[timestamp_start, timestamp_stop]).aggregate(
        humidity=Avg('humidity'),
        airQuality=Avg('airQuality'),
        temperature=Avg('temperature'),
        at=Avg('tStamp'))
    if averages['humidity'] == None:
        raise Exception('No any data')
    humidity = int(averages['humidity'])
    temperature = int(averages['temperature'])
    airQuality = int(averages['airQuality'])
    averages.update({
        'humidity': {
            'value': humidity,
            'size': humidity / 100,
            'color': "#E4766E" if humidity > 85 else "#B4D572"
        },
        'temperature': {
            'value': temperature,
            'size': temperature / 25,
            'color': "#E4766E" if temperature > 15 else "#B4D572"
        },
        'airQuality': {
            'value': airQuality,
            'size': airQuality / 2500,
            'color': "#E4766E" if airQuality > 1200 else "#B4D572"
        },
        'from': datetime.fromtimestamp(timestamp_start),
        'to': datetime.fromtimestamp(timestamp_stop)
    })
    return averages


def __append_to_result(r, start, stop, result):
    for elt in range(r):
        timestamp_start = start(elt)
        timestamp_stop = stop(elt)
        averages = __averages_by_timestamps(
            timestamp_start, timestamp_stop)
        result['averages'].append(averages)


def __get_datas(interval, start):
    if type(start) != "int":
        start = int(start)

    result = {
        'start': start,
        'start_date':  datetime.fromtimestamp(start).strftime("%Y-%m-%dT%H:%M"),
        'averages': []
    }

    if interval == "hour":
        def timestamp_start(hour)-> int: return start - (hour + 1) * 60 * 60
        def timestamp_stop(hour)-> int: return start - hour * 60 * 60
        r = 24

    elif interval == "day":
        def timestamp_start(day)-> int: return start - (day + 1) * 24 * 60 * 60
        def timestamp_stop(day) -> int: return start - day * 24 * 60 * 60
        r = 7
    elif interval == "week":
        def timestamp_start(week) -> int: return start - (week + 1) * 7 * 24 * 60 * 60
        def timestamp_stop(week) -> int: return start - week * 7 * 24 * 60 * 60
        r = 10
    try:
        __append_to_result(r, timestamp_start, timestamp_stop, result)
    except:
        print('No data')
    return result


def home(request):
    last_data = None
    try:
        last_data = datas.objects.order_by('-id')[0]
    except IndexError:
        # return no data html
        return None

    interval = start = settings = None
    try:
        interval = request.GET['interval']
    except KeyError:
        return redirect(__replace_query_param(request.get_full_path(), 'interval', 'day'))
    try:
        start = request.GET['start']
    except KeyError:
        return redirect(__replace_query_param(request.get_full_path(), 'start', int(time())))
    try:
        settings = request.GET['settings'] == "True"
    except KeyError:
        return redirect(__replace_query_param(request.get_full_path(), 'settings', False))

    content: dict = __get_datas(interval, start)

    content.update({
        'interval': interval,
        'settings': settings,
        'waterPercent': int(last_data.humidity),
        'temperaturePercent': int(last_data.temperature),
        'qualityDeg': int(last_data.airQuality * 180 / 2000),
        'qualityDegValue': int(last_data.airQuality),
        'links': {
            'hour': __replace_query_param(request.get_full_path(), 'interval', 'hour'),
            'day': __replace_query_param(request.get_full_path(), 'interval', 'day'),
            'week': __replace_query_param(request.get_full_path(), 'interval', 'week'),
            'sensors':'/sensors',
            'settings': {
                'true': __replace_query_param(request.get_full_path(), 'settings', 'True'),
                'false': __replace_query_param(request.get_full_path(), 'settings', 'False')
            }
        }
    })

    return render(request, 'home/home.html', content)


def createDatas(request):
    now = int(time())
    end = now - 432000000
    print('Start create data from {now} to {end}'.format(now=now, end=end))
    timeInterval = [end, now]
    # DECOMMENTER POUR ACTIVER LA CREATION DE DONNEES
    html = """
    <html>
    <body>
        <table>
            <thead>
                <tr>
                    <th> air quality </th>
                    <th> temperature </th>
                    <th> humidity </th>
                </tr>
            </thead>
            <tbody>
    """
    count = 0
    for row in range(timeInterval[0], timeInterval[1], 1000):
        if count % 1000 == 0:
            print('Generated values: ', count)
        airQuality = random.randint(800, 1500)
        temperature = random.randint(15, 18)
        humidity = random.randint(85, 90)
        d = datas(sensor_id='24:6F:28:24:6B:50', tStamp=row,
                  airQuality=airQuality, humidity=humidity, temperature=temperature)
        html += """
        <tr>
            <td>{air}</td>
            <td>{temperature}</td>
            <td>{humidity}</td>
        </tr>
        """.format(air=airQuality, temperature=temperature, humidity=humidity)
        count += 1
        d.save()

    html += '</tbody></table></body></html>'

    return HttpResponse(html)

def sensors(request):
    if request.method == "GET":
        interval = mac = name = None
        try:
            mac = request.GET['mac']
        except KeyError:
            print()
        try:
            name = request.GET['name']
        except KeyError:
            print()
        try:
            interval = request.GET['interval']
        except KeyError:
            print()
        
        content: dict = {
            'mac': mac,
            'name': name,
            'interval': interval,
            
            'links': {
                'sensors':'/sensors',
                'home': '/'
            }
        }
        
        content['sensors'] = sensor.objects.all()
        _sensors = []
        for _sensor in content['sensors']:
            delete_link = __replace_query_param('/sensors/delete', 'mac', _sensor.macAddress)
            full_link = __replace_query_param(request.get_full_path(), 'mac', _sensor.macAddress)
            full_link = __replace_query_param(delete_link, 'name', _sensor.name)
            full_link = __replace_query_param(full_link, 'interval', _sensor.interval)
            _sensors.append({
                'name': _sensor.name,
                'mac': _sensor.macAddress,
                'interval': _sensor.interval,
                'link': {
                    'edit': full_link,
                    'delete': delete_link
                }
            })
        content['sensors'] = _sensors
        content.update({
            'test': str(content)
        })
  
        return render(request, 'sensor/sensor.html', content)
    
    elif request.method == "POST":
        mac = request.POST.get('sensor_mac')
        name = request.POST.get('sensor_name')
        interval = request.POST.get('sensor_interval')
        s = sensor.create(mac, name, interval)
        s.save()
        return redirect('/sensors')

    
def delete(request):
    mac = None
    try:
        mac = request.GET['mac']
    except KeyError:
        return redirect('/sensors')
    sensor.objects.get(macAddress=mac).delete()
    return redirect('/sensors')
        