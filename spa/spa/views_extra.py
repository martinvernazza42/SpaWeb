from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from .models import Cliente, Turno, Profesional
from .utils import render_to_pdf

@login_required
def historial_cliente_pdf(request, cliente_id):
    """Genera un PDF con el historial de un cliente"""
    user = request.user
    
    # Solo accesible para profesionales
    if not hasattr(user, 'profesional'):
        messages.error(request, "No tienes permiso para acceder a esta sección")
        return redirect('index')
    
    prof = user.profesional
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    # Obtener todos los turnos de este cliente con este profesional
    turnos = Turno.objects.filter(
        cliente=cliente,
        profesional=prof
    ).order_by('-fecha', '-hora')
    
    context = {
        'cliente': cliente,
        'turnos': turnos,
        'profesional': prof
    }
    
    pdf = render_to_pdf('pdf_historial_cliente.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"historial_{cliente.user.last_name}_{cliente.user.first_name}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error al generar el PDF", status=400)

@login_required
def guardar_comentario_turno(request, turno_id):
    """Guarda un comentario para un turno específico"""
    user = request.user
    
    # Solo accesible para profesionales
    if not hasattr(user, 'profesional'):
        messages.error(request, "No tienes permiso para acceder a esta sección")
        return redirect('index')
    
    prof = user.profesional
    turno = get_object_or_404(Turno, pk=turno_id, profesional=prof)
    
    if request.method == 'POST':
        comentario = request.POST.get('comentario', '').strip()
        turno.comentario = comentario
        turno.save()
        messages.success(request, "Comentario guardado correctamente")
    
    # Redirigir de vuelta al historial del cliente
    return redirect(f"{reverse('historial_clientes')}?cliente_id={turno.cliente.id}")