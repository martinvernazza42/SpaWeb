# spa/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('consultas/', views.consultas, name='consultas'),
    path('turnos/', views.turnos, name='turnos'),
    path('perfil/', views.perfil, name='perfil'),
    path('servicios/individuales/', views.servicios_individuales, name='servicios_individuales'),
    path('servicios/grupales/', views.servicios_grupales, name='servicios_grupales'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
]
