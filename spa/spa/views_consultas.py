from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from urllib.parse import quote
from .models import Consulta, Servicio

def consulta_view(request):
    # Obtener todos los servicios para el selector
    servicios = Servicio.objects.all().order_by('nombre')
    
    if request.method == "POST":
        servicio_id = request.POST.get('servicio_id')
        mensaje = request.POST.get('mensaje')
        
        # Si el usuario está autenticado, usar sus datos
        if request.user.is_authenticated:
            nombre = request.user.get_full_name() or request.user.username
            email = request.user.email
        else:
            # Si no está autenticado, obtener del formulario
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
        
        # Crear la consulta
        consulta = Consulta(nombre=nombre, email=email, mensaje=mensaje)
        
        # Asignar servicio si se seleccionó uno
        if servicio_id:
            try:
                servicio = Servicio.objects.get(pk=servicio_id)
                consulta.servicio = servicio
            except Servicio.DoesNotExist:
                pass
                
        consulta.save()
        messages.success(request, 'Tu consulta ha sido enviada correctamente. ¡Gracias!')
        return redirect('consultas')
    
    # Filtrar mensajes para mostrar solo los relacionados con consultas
    storage = messages.get_messages(request)
    for message in storage:
        if 'consulta' not in message.message.lower() and 'gracias' not in message.message.lower():
            storage.used = False
    
    return render(request, 'consultas.html', {
        'servicios': servicios,
        'user_authenticated': request.user.is_authenticated
    })

@login_required
def consultas_profesional(request):
    """Vista para que los profesionales vean las consultas de su servicio"""
    user = request.user
    
    # Solo accesible para profesionales
    if not hasattr(user, 'profesional'):
        messages.error(request, "No tienes permiso para acceder a esta sección")
        return redirect('index')
    
    prof = user.profesional
    servicio = prof.servicio
    
    # Obtener consultas relacionadas con el servicio del profesional
    consultas_pendientes = Consulta.objects.filter(
        servicio=servicio,
        respondida=False
    ).order_by('-fecha_creacion')
    
    consultas_respondidas = Consulta.objects.filter(
        servicio=servicio,
        respondida=True
    ).order_by('-fecha_creacion')
    
    return render(request, 'consultas_profesional.html', {
        'servicio': servicio,
        'consultas_pendientes': consultas_pendientes,
        'consultas_respondidas': consultas_respondidas
    })

@login_required
def responder_consulta(request, consulta_id):
    """Vista para responder a una consulta"""
    user = request.user
    
    # Solo accesible para profesionales
    if not hasattr(user, 'profesional'):
        messages.error(request, "No tienes permiso para acceder a esta sección")
        return redirect('index')
    
    prof = user.profesional
    servicio = prof.servicio
    
    # Verificar que la consulta pertenezca al servicio del profesional
    consulta = get_object_or_404(Consulta, pk=consulta_id, servicio=servicio)
    
    if request.method == 'POST':
        asunto = request.POST.get('asunto', f"Re: Consulta sobre {servicio.nombre}")
        mensaje = request.POST.get('mensaje', '')
        
        # Codificar para URL
        asunto_encoded = quote(asunto)
        mensaje_encoded = quote(mensaje)
        
        # Crear URL de Gmail
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={consulta.email}&su={asunto_encoded}&body={mensaje_encoded}"
        
        # Marcar como respondida
        consulta.respondida = True
        consulta.save()
        
        # Redirigir al usuario a Gmail
        return redirect(gmail_url)
    
    return render(request, 'responder_consulta.html', {
        'consulta': consulta,
        'servicio': servicio,
        'user': user
    })