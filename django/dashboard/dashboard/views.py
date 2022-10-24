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
    # Fonction qui récupère les datas brutes, les traite et renvoi un dict formaté pour utiliser avec le graf

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
            sizeHumidity = row.humidity/100 # Formules de calcul de la taille colonne 
            sizeTemp = row.temperature/25 
            sizeAirQ = row.airQuality/2500
            date = datetime.fromtimestamp(row.tStamp)     
            date = date.strftime("%d/%m/%y : %H")
            if sizeHumidity > 0.85 : 
                colorH = "#E4766E"
            else : 
                colorH = "#B4D572"
            
            if sizeTemp> 0.6 :  # Température supérieure à 15°C (15*4/100 = 0.6)
                colorT = '#E4766E'
            else : 
                colorT = '#B4D572'

            if sizeAirQ> 0.48 : # AirQ sup à 1200 (1200*4/10000)
                colorA = '#E4766E'
            else : 
                colorA = '#B4D572' 


            humidityDatas.append({'color' : colorH, 'size' : sizeHumidity, 'datas': row.humidity, 'date' : date, 'showLabel' : showLabel })
            tempDatas.append({'color' : colorT, 'size' : sizeTemp, 'datas': row.temperature, 'date' : date, 'showLabel' : showLabel })
            airQDatas.append({'color' : colorA, 'size' : sizeAirQ, 'datas': row.airQuality, 'date' : date, 'showLabel' : showLabel })
       

        
        
    return {'sensorList':sensorList, 'humidityDatas' : humidityDatas, 'tempDatas' : tempDatas , 'airQDatas':airQDatas}


def testGraf(request):
    #Exemple d'utilisation de getDatas 
    return render (request, 'testGraf/testGraf.html', getDatas("day",1646109200))



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

