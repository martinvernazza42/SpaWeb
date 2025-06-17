from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import views_consultas

urlpatterns = [
    # Secciones generales
    path('', views.index, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path(
        'servicios/<int:servicio_id>/calendario/',
        views.calendario_servicio,
        name='calendario_servicio'
    ),
    path(
        'servicios/<int:servicio_id>/calendario/<int:year>/<int:month>/<int:day>/reservar/',
        views.reservar_por_fecha,
        name='reservar_por_fecha'
    ),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('turnos/', views.turnos, name='turnos'),
    path('consultas/', views_consultas.consulta_view, name='consultas'),
    path('mis-consultas/', views_consultas.consultas_profesional, name='consultas_profesional'),
    path('responder-consulta/<int:consulta_id>/', views_consultas.responder_consulta, name='responder_consulta'),

    # Reserva
    path(
        'turno/<int:turno_id>/confirmacion/',
        views.reserva_exitosa,
        name='reserva_exitosa'
    ),

    # Método de pago simulado
    path(
        'servicio/<int:servicio_id>/pagar/<str:fecha_str>/<int:slot_id>/',
        views.pagar_turno,
        name='pagar_turno'
    ),

    # Administración de turnos (solo staff)
    path(
        'admin/servicios/<int:servicio_id>/turnos/',
        views.admin_lista_turnos,
        name='admin_lista_turnos'
    ),
    path(
        'admin/servicios/<int:servicio_id>/turnos/nuevo/',
        views.admin_editar_turno,
        name='admin_crear_turno'
    ),
    path(
        'admin/turnos/<int:turno_id>/editar/',
        views.admin_editar_turno,
        name='admin_editar_turno'
    ),
    path(
        'admin/turnos/<int:turno_id>/eliminar/',
        views.admin_eliminar_turno,
        name='admin_eliminar_turno'
    ),

    # Panel de administración personalizado
    path('panel-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('panel-admin/servicios/', views.admin_servicios, name='admin_servicios'),
    path('panel-admin/turnos/', views.admin_turnos, name='admin_turnos'),
    path('panel-admin/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('panel-admin/consultas/', views.admin_consultas, name='admin_consultas'),
    
    # PDFs de turnos
    path('panel-admin/turnos/pdf/<int:turno_id>/', views.turno_pdf, name='turno_pdf'),
    path('panel-admin/turnos/pdf/', views.turnos_lista_pdf, name='turnos_lista_pdf'),
    
    # Responder consultas
    path('panel-admin/consultas/responder/<int:consulta_id>/', views.admin_responder_consulta, name='admin_responder_consulta'),
    
    # Historial de clientes para profesionales
    path('historial-clientes/', views.historial_clientes, name='historial_clientes'),
    path('historial-clientes/pdf/<int:cliente_id>/', views.historial_cliente_pdf, name='historial_cliente_pdf'),
    path('guardar-comentario/<int:turno_id>/', views.guardar_comentario_turno, name='guardar_comentario_turno'),
    
    # Django admin (oculto)
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

    # API del chatbot
    path('api/chat/', include('chatbot.urls')),
    path('cart/add/<int:servicio_id>/<str:fecha>/<str:hora>/', views.add_to_cart, name='cart_add'),
    path('cart/',     views.view_cart,    name='view_cart'),
    path('cart/pay/', views.checkout,     name='cart_checkout'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)