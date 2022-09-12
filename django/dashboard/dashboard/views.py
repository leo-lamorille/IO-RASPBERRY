from django.http import HttpResponse
from django.shortcuts import render

def dashboard(request):
    return HttpResponse('<h1>Dashboard is working!</h1>')

def admin(request):
    return HttpResponse('<h1>Admin is working!</h1>')