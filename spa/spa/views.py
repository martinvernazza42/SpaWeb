# spa/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def servicios(request):
    return render(request, 'servicios.html')

def consultas(request):
    return render(request, 'consultas.html')

def turnos(request):
    return render(request, 'turnos.html')

def perfil(request):
    return render(request, 'perfil.html')
