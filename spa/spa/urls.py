from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Secciones generales
    path('', views.index, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('servicios/<int:servicio_id>/calendario/', views.calendario_servicio, name='calendario_servicio'),
    path(
        'servicios/<int:servicio_id>/calendario/<int:year>/<int:month>/<int:day>/reservar/',
        views.reservar_por_fecha,
        name='reservar_por_fecha'
    ),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('turnos/', views.turnos, name='turnos'),
    path('consultas/', views.consulta_view, name='consultas'),

    # Reserva
    path('turno/<int:turno_id>/confirmacion/', views.reserva_exitosa, name='reserva_exitosa'),

    # Método de pago simulado
    path('servicio/<int:servicio_id>/pagar/<str:fecha_str>/<int:slot_id>/', views.pagar_turno, name='pagar_turno'),

    # Administración de turnos (solo staff)
    path('admin/servicios/<int:servicio_id>/turnos/',
         views.admin_lista_turnos,
         name='admin_lista_turnos'),
    path('admin/servicios/<int:servicio_id>/turnos/nuevo/',
         views.admin_editar_turno,
         name='admin_crear_turno'),
    path('admin/turnos/<int:turno_id>/editar/',
         views.admin_editar_turno,
         name='admin_editar_turno'),
    path('admin/turnos/<int:turno_id>/eliminar/',
         views.admin_eliminar_turno,
         name='admin_eliminar_turno'),

    # Django admin
    path('admin/', admin.site.urls),

    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Perfil de usuario
    path('perfil/', views.perfil, name='perfil'),
    path('mis-turnos/', views.mis_turnos, name='mis_turnos'),

    path(
    'servicio/<int:servicio_id>/elegir-pago/<str:fecha_str>/<int:slot_id>/',
    views.elegir_pago,
    name='elegir_pago'
),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
