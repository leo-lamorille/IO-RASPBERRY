from django.shortcuts import render
from dashboard.models import sensor, datas
from django.http import HttpResponse
import random
from datetime import datetime, timedelta

def dashboard(request):
    data = datas.objects.order_by('-id')[0]
    return render(request, 'dashboard/dashboard.html', {'waterPercent': int(data.humidity), 'temperaturePercent': int(data.temperature), 'qualityDeg': int(data.airQuality * 180 / 2000), 'qualityDegValue': int(data.airQuality)})

def admin(request):
    return render(request, 'admin/admin.html')


def getDatas(interval, dateDebut) :  # Passer une date en format string YYYY-MM-DD 

    # if type(dateDebut) != "int" : 
    #     dateDebut = int(dateDebut)
    dateFin = datetime.fromtimestamp(dateDebut)
    if interval == "day":
        dateFin = dateFin + timedelta(days=1)
        dateFin = datetime.timestamp(dateFin)
        datasList = datas.objects.filter(tStamp__gte=dateDebut, tStamp__lte = dateFin)

    if interval == "week":
        dateFin = dateFin + timedelta(days=7)
        dateFin = datetime.timestamp(dateFin)
        datasList = datas.objects.filter(tStamp__gte=dateDebut, tStamp__lte = dateFin)

    if interval == "month":
        dateFin = dateFin + timedelta(days = 30)
        dateFin = datetime.timestamp(dateFin)
        datasList = datas.objects.filter(tStamp__gte=dateDebut, tStamp__lte = dateFin)



    sensorList = sensor.objects.all() # Importe la liste des capteurs {'macAdress', 'naùe, 'interval'}
    humidityDatas = []
    tempDatas = []
    airQDatas = []
    showLabel = "" # Permet d'afficher ou non certains labels date 

    for rank, row  in enumerate(datasList) : 
        if interval == "day" and  rank%360==0 or interval == "week" and rank%4200 == 0 or interval == "month" and rank %8600 == 0 : 
            sizeHumidity = row.humidity/100
            sizeTemp = row.temperature/100 #v
            sizeAirQ = row.airQuality/10000
            date = datetime.fromtimestamp(row.tStamp)     
            date = date.strftime("%d/%m/%y : %H")
            if sizeHumidity > 0.8 : 
                colorH = "#E4766E"
            else : 
                colorH = "#B4D572"
            
            if sizeTemp> 0.1 : 
                colorT = 'red'
            else : 
                colorT = 'blue'

            if sizeAirQ> 0.15 : 
                colorA = 'red'
            else : 
                colorA = 'blue' 

            humidityDatas.append({'color' : colorH, 'size' : sizeHumidity, 'humidity': row.humidity, 'date' : date, 'showLabel' : showLabel })
            tempDatas.append({'color': colorT, 'size' : sizeTemp})
            airQDatas.append({'color': colorA, 'size' : sizeAirQ})
       

        
        
    return {'sensorList':sensorList, 'humidityDatas' : humidityDatas, 'tempDatas' : tempDatas , 'airQDatas':airQDatas}


def testGraf(request):


    return render (request, 'testGraf/testGraf.html', getDatas("week",1646179200))


def test(request):
    sensorList = sensor.objects.all() # Importe la liste des capteurs {'macAdress', 'naùe, 'interval'}
    datasList = datas.objects.all()  #Importe les datas brutes {'sensor', 't_stamp', 'value'}
    renderGraf = testGraf(request)
    return render (request, 'dashboard/test.html', {'sensorList':sensorList, 'datas' : datasList, 'renderGraf':renderGraf})


def createDatas(request):
    timeInterval = [1646089200, 1649541600]
    ####### DECOMMENTER POUR ACTIVER LA CREATION DE DONNEES 


    # for row in range(timeInterval[0], timeInterval[1], 10):
    #     airQuality = random.randint(800,1500)
    #     temperature = random.randint(15,18)
    #     humidity = random.randint(85,90)
    #     d = datas(sensor_id='24:6F:28:24:6B:50', tStamp = row , airQuality= airQuality, humidity = humidity, temperature = temperature)
    #     d.save()

    datasList = datas.objects.all()
    html = "<html><body>"
    for row in datasList :
        html += "<div> %s </div>" % str(row.tStamp)
    html+= '</body></html>'
      
    return HttpResponse(html)

