from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def admin(request):
    return render(request, 'admin/admin.html')