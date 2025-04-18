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

def inicio(request):
    return render(request, 'base.html')

def servicios_individuales(request):
    return render(request, 'servicios_individuales.html')

def servicios_grupales(request):
    return render(request, 'servicios_grupales.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')