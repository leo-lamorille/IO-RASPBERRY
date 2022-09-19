from django.shortcuts import render
from dashboard.models import sensor, datas

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def admin(request):
    return render(request, 'admin/admin.html')

def test(request):
    sensorList = sensor.objects.all()
    return render (request, 'dashboard/test.html', {'sensorList':sensorList})