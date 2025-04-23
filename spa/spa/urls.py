from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('consultas/', views.consultas, name='consultas'),
    
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
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'), 
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
    
    #Carga de foto en servicios
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)