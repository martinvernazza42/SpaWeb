# spa/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('consultas/', views.consultas, name='consultas'),
    path('turnos/', views.turnos, name='turnos'),
    path('perfil/', views.perfil, name='perfil'),
]
