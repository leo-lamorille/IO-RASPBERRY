from django.shortcuts import render
from dashboard.models import sensor, datas

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def admin(request):
    return render(request, 'admin/admin.html')

def test(request):
    sensorList = sensor.objects.all() # Importe la liste des capteurs {'macAdress', 'naùe, 'interval'}
    datas = datas.objects.all()  #Importe les datas brutes {'sensor', 't_stamp', 'value'}
    return render (request, 'dashboard/test.html', {'sensorList':sensorList, 'datas' : datas})