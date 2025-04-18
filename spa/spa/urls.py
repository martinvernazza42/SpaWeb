from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Inicio y secciones
    path('', views.index, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path(
        'servicios/<int:servicio_id>/calendario/',
        views.calendario_servicio,
        name='calendario_servicio'
    ),
    # Ruta para reservar un día concreto
    path(
        'servicios/<int:servicio_id>/calendario/'
        '<int:year>/<int:month>/<int:day>/reservar/',
        views.reservar_por_fecha,
        name='reservar_por_fecha'
    ),

      path(
        'turno/<int:turno_id>/confirmacion/',
        views.reserva_exitosa,
        name='reserva_exitosa'
    ),

    path('consultas/', views.consultas, name='consultas'),
    path('turnos/',    views.turnos,    name='turnos'),

    # Auth
    path('registro/', views.registro, name='registro'),
    path('login/',    views.login_view,  name='login'),
    path('logout/',   views.logout_view, name='logout'),

    path(
      'mis-turnos/',
      views.mis_turnos,
      name='mis_turnos'
    ),

    # Perfil
    path('perfil/',   views.perfil,    name='perfil'),
]
