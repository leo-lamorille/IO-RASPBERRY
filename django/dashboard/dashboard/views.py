from django.shortcuts import render
from dashboard.models import sensor, datas
from django.http import HttpResponse
import random

import datetime
def dashboard(request):
    data = datas.objects.order_by('-id')[0]
    return render(request, 'dashboard/dashboard.html', {'waterPercent': int(data.humidity), 'temperaturePercent': int(data.temperature), 'qualityDeg': int(data.airQuality * 180 / 2000), 'qualityDegValue': int(data.airQuality)})

def admin(request):
    return render(request, 'admin/admin.html')

def test(request):
    sensorList = sensor.objects.all() # Importe la liste des capteurs {'macAdress', 'naùe, 'interval'}
    datasList = datas.objects.all()  #Importe les datas brutes {'sensor', 't_stamp', 'value'}
    return render (request, 'dashboard/test.html', {'sensorList':sensorList, 'datas' : datasList})


def createDatas(request):
    timeInterval = [1664143700138, 1664199800138]
    ####### DECOMMENTER POUR ACTIVER LA CREATION DE DONNEES 


    # for row in range(timeInterval[0], timeInterval[1], 10000):
    #     airQuality = random.randint(800,850)
    #     temperature = random.randint(15,18)
    #     humidity = random.randint(85,90)
    #     d = datas(sensor_id='00:00:00:00:00:00', tStamp = row , airQuality= airQuality, humidity = humidity, temperature = temperature)
    #     d.save()

    datasList = datas.objects.all()
    html = "<html><body>"
    for row in datasList :
        html += "<div> %s </div>" % str(row.tStamp)
    html+= '</body></html>'
      
    return HttpResponse(html)

def testGraf(request):
    return render(request, 'testGraf/testGraf.html')
