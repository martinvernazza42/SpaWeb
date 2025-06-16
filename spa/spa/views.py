import calendar
from datetime import datetime, timedelta, date as _date
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from .models import (
    Servicio, Turno, Cart, CartItem,
    SubcategoriaServicio, Disponibilidad,
    Cliente, Consulta, Profesional
)
from .forms import (
    CustomAuthForm, RegistroUsuarioForm,
    ConsultaForm, DisponibilidadForm,
    PagoForm
)

# -------------------------------------------------------------------
# Vistas Públicas
# -------------------------------------------------------------------

def index(request):
    return render(request, 'index.html')


def servicios(request):
    subcategoria_id = request.GET.get('subcategoria')

    if subcategoria_id:
        current_subcategoria = get_object_or_404(SubcategoriaServicio, pk=subcategoria_id)
        servicios = Servicio.objects.filter(subcategoria=current_subcategoria)
    else:
        current_subcategoria = None
        servicios = Servicio.objects.all()

    subcategorias = SubcategoriaServicio.objects.all()

    return render(request, 'servicios.html', {
        'servicios': servicios,
        'subcategorias': subcategorias,
        'current_subcategoria': current_subcategoria,
    })


def quienes_somos(request):
    return render(request, 'quienes_somos.html')


def consulta_view(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        Consulta(nombre=nombre, email=email, mensaje=mensaje).save()
        messages.success(request, 'Tu consulta ha sido enviada correctamente. ¡Gracias!')
        return redirect('consultas')
    return render(request, 'consultas.html')


def turnos(request):
    return render(request, 'turnos.html')


@login_required
def calendario_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    hoy = _date.today()
    ahora = timezone.now()

    try:
        year = int(request.GET.get('year', hoy.year))
    except ValueError:
        year = hoy.year
    try:
        month = int(request.GET.get('month', hoy.month))
    except ValueError:
        month = hoy.month

    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)

    qs = Disponibilidad.objects.filter(
        servicio=servicio,
        fecha__year=year,
        fecha__month=month
    )

    disponibles = []
    cutoff = ahora + timedelta(hours=48)
    for d in qs:
        slot_dt = datetime.combine(d.fecha, d.hora_inicio)
        if timezone.is_naive(slot_dt):
            slot_dt = timezone.make_aware(slot_dt)
        if slot_dt >= cutoff:
            ya_tomado = Turno.objects.filter(
                servicio=servicio,
                fecha=d.fecha,
                hora=d.hora_inicio
            ).exists()
            if not ya_tomado:
                disponibles.append(d)

    available = {d.fecha.day for d in disponibles}

    return render(request, 'calendario_servicio.html', {
        'servicio': servicio,
        'year': year,
        'month': month,
        'month_days': month_days,
        'available': available,
        'day_names': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    })


@login_required
def reservar_por_fecha(request, servicio_id, year, month, day):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    fecha_obj = _date(year, month, day)

    todos_los_slots = Disponibilidad.objects.filter(servicio=servicio, fecha=fecha_obj)
    slots = [slot for slot in todos_los_slots if not Turno.objects.filter(
        servicio=servicio,
        fecha=fecha_obj,
        hora=slot.hora_inicio
    ).exists()]

    ahora = timezone.now()
    cutoff = ahora + timedelta(hours=48)

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        slot = get_object_or_404(Disponibilidad, pk=slot_id)

        slot_dt = datetime.combine(slot.fecha, slot.hora_inicio)
        if timezone.is_naive(slot_dt):
            slot_dt = timezone.make_aware(slot_dt)
        if slot_dt < cutoff:
            messages.error(request, 'Las reservas deben hacerse con al menos 48 hs de anticipación.')
            return redirect('calendario_servicio', servicio_id=servicio.id)

        cliente, _ = Cliente.objects.get_or_create(user=request.user)
        fecha_str = fecha_obj.strftime("%Y-%m-%d")
        return redirect('elegir_pago', servicio_id=servicio.id, fecha_str=fecha_str, slot_id=slot.id)

    return render(request, 'reservar_por_fecha.html', {
        'servicio': servicio,
        'day': fecha_obj,
        'slots': slots,
    })


@login_required
def reserva_exitosa(request, turno_id):
    turno = get_object_or_404(
        Turno,
        pk=turno_id,
        cliente__user=request.user
    )
    return render(request, 'reserva_exitosa.html', {'turno': turno})


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('login')

login_view = auth_views.LoginView.as_view(
    template_name='login.html',
    authentication_form=CustomAuthForm,
)

@login_required
def perfil(request):
    turnos = Turno.objects.filter(cliente=request.user.cliente)
    consultas = Consulta.objects.filter(email=request.user.email)
    return render(request, 'perfil.html', {
        'turnos': turnos,
        'consultas': consultas
    })

@login_required
def mis_turnos(request):
    user = request.user

    # Si es Profesional, muestro los turnos de su servicio en la semana actual
    if hasattr(user, 'profesional'):
        prof = user.profesional
        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana    = inicio_semana + timedelta(days=14)

        turnos = Turno.objects.filter(
            servicio=prof.servicio,
            fecha__range=(inicio_semana, fin_semana)
        ).order_by('fecha', 'hora')

        return render(request, 'profesional_turnos.html', {
            'turnos': turnos,
            'servicio': prof.servicio,
            'inicio_semana': inicio_semana,
            'fin_semana': fin_semana,
        })

    # Si no es Profesional, asumo que es Cliente
    cliente = get_object_or_404(Cliente, user=user)
    turnos = Turno.objects.filter(cliente=cliente).order_by('fecha', 'hora')
    return render(request, 'mis_turnos.html', {
        'turnos': turnos
    })

@staff_member_required
def admin_dashboard(request):
    # Contar servicios
    total_servicios = Servicio.objects.count()
    
    # Contar clientes (usuarios que no son staff y no son profesionales)
    total_clientes = Cliente.objects.count()
    
    # Contar consultas
    total_consultas = Consulta.objects.count()
    
    # Contar turnos de hoy
    hoy = timezone.now().date()
    turnos_hoy = Turno.objects.filter(fecha=hoy).count()
    
    # Obtener los próximos turnos para mostrar en la tabla
    turnos_proximos = Turno.objects.filter(fecha__gte=hoy).order_by('fecha', 'hora')[:10]
    
    # Obtener servicios para mostrar en la tabla
    servicios = Servicio.objects.all()
    
    return render(request, 'admin/dashboard.html', {
        'servicios': servicios,
        'turnos_proximos': turnos_proximos,
        'total_servicios': total_servicios,
        'total_clientes': total_clientes,
        'total_consultas': total_consultas,
        'turnos_hoy': turnos_hoy,
        'hoy': hoy,
        'active_tab': 'dashboard'
    })

@staff_member_required
def admin_servicios(request):
    servicios = Servicio.objects.all().order_by('subcategoria__nombre', 'nombre')
    subcategorias = SubcategoriaServicio.objects.all()
    
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio_id')
        action = request.POST.get('action')
        
        # Eliminar servicio
        if action == 'delete' and servicio_id:
            servicio = get_object_or_404(Servicio, pk=servicio_id)
            servicio.delete()
            messages.success(request, f"El servicio '{servicio.nombre}' ha sido eliminado.")
            return redirect('admin_servicios')
        
        # Editar servicio
        if servicio_id:
            servicio = get_object_or_404(Servicio, pk=servicio_id)
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            subcategoria_id = request.POST.get('subcategoria')
            
            if nombre and descripcion and precio and subcategoria_id:
                try:
                    subcategoria = get_object_or_404(SubcategoriaServicio, pk=subcategoria_id)
                    
                    servicio.nombre = nombre
                    servicio.descripcion = descripcion
                    servicio.precio = precio
                    servicio.subcategoria = subcategoria
                    
                    # Manejar la imagen si se proporciona una nueva
                    if 'imagen' in request.FILES:
                        servicio.imagen = request.FILES['imagen']
                    
                    servicio.save()
                    messages.success(request, f"El servicio '{nombre}' ha sido actualizado.")
                except Exception as e:
                    messages.error(request, f"Error al actualizar el servicio: {str(e)}")
                
                return redirect('admin_servicios')
        
        # Crear nuevo servicio
        if 'action' not in request.POST:
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            subcategoria_id = request.POST.get('subcategoria')
            
            if nombre and descripcion and precio and subcategoria_id:
                try:
                    subcategoria = get_object_or_404(SubcategoriaServicio, pk=subcategoria_id)
                    
                    servicio = Servicio(
                        nombre=nombre,
                        descripcion=descripcion,
                        precio=precio,
                        subcategoria=subcategoria
                    )
                    
                    if 'imagen' in request.FILES:
                        servicio.imagen = request.FILES['imagen']
                    
                    servicio.save()
                    messages.success(request, f"El servicio '{nombre}' ha sido creado.")
                except Exception as e:
                    messages.error(request, f"Error al crear el servicio: {str(e)}")
                
                return redirect('admin_servicios')
    
    return render(request, 'admin/servicios.html', {
        'servicios': servicios,
        'subcategorias': subcategorias,
        'active_tab': 'servicios'
    })

from django.http import HttpResponse
from urllib.parse import quote
from django.contrib.auth.models import User
from .utils import render_to_pdf

@staff_member_required
def admin_turnos(request):
    hoy = timezone.now().date()
    
    # Procesar formularios POST (editar o eliminar turno)
    if request.method == 'POST':
        turno_id = request.POST.get('turno_id')
        action = request.POST.get('action')
        
        if turno_id:
            turno = get_object_or_404(Turno, pk=turno_id)
            
            # Eliminar turno
            if action == 'delete':
                turno.delete()
                messages.success(request, "El turno ha sido eliminado correctamente.")
                return redirect('admin_turnos')
            
            # Editar turno
            cliente_id = request.POST.get('cliente')
            servicio_id = request.POST.get('servicio')
            fecha_str = request.POST.get('fecha')
            hora_str = request.POST.get('hora')
            
            if cliente_id and servicio_id and fecha_str and hora_str:
                try:
                    cliente = get_object_or_404(Cliente, pk=cliente_id)
                    servicio = get_object_or_404(Servicio, pk=servicio_id)
                    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                    hora = datetime.strptime(hora_str, '%H:%M').time()
                    
                    turno.cliente = cliente
                    turno.servicio = servicio
                    turno.fecha = fecha
                    turno.hora = hora
                    turno.save()
                    
                    messages.success(request, "El turno ha sido actualizado correctamente.")
                except Exception as e:
                    messages.error(request, f"Error al actualizar el turno: {str(e)}")
                
                return redirect('admin_turnos')
    
    # Obtener fechas del filtro
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    # Filtrar turnos según las fechas proporcionadas
    if fecha_desde and fecha_hasta:
        try:
            fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            turnos = Turno.objects.filter(fecha__range=(fecha_desde, fecha_hasta)).order_by('fecha', 'hora')
        except ValueError:
            # Si hay un error en el formato de fecha, mostrar todos los turnos futuros
            turnos = Turno.objects.filter(fecha__gte=hoy).order_by('fecha', 'hora')
    else:
        # Por defecto, mostrar turnos futuros
        turnos = Turno.objects.filter(fecha__gte=hoy).order_by('fecha', 'hora')
    
    servicios = Servicio.objects.all()
    clientes = Cliente.objects.all()
    
    return render(request, 'admin/turnos.html', {
        'turnos': turnos,
        'servicios': servicios,
        'clientes': clientes,
        'fecha_desde': fecha_desde if fecha_desde else '',
        'fecha_hasta': fecha_hasta if fecha_hasta else '',
        'active_tab': 'turnos'
    })

@staff_member_required
def turno_pdf(request, turno_id):
    turno = get_object_or_404(Turno, pk=turno_id)
    context = {'turno': turno}
    pdf = render_to_pdf('admin/pdf_turno.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"turno_{turno.id}_{turno.cliente}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error al generar el PDF", status=400)

@staff_member_required
def turnos_lista_pdf(request):
    hoy = timezone.now().date()
    
    # Obtener fechas del filtro
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    # Filtrar turnos según las fechas proporcionadas
    if fecha_desde and fecha_hasta:
        try:
            fecha_desde_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            turnos = Turno.objects.filter(fecha__range=(fecha_desde_obj, fecha_hasta_obj)).order_by('fecha', 'hora')
            filename = f"turnos_{fecha_desde}_a_{fecha_hasta}.pdf"
        except ValueError:
            turnos = Turno.objects.filter(fecha__gte=hoy).order_by('fecha', 'hora')
            filename = f"lista_turnos_{hoy}.pdf"
    else:
        turnos = Turno.objects.filter(fecha__gte=hoy).order_by('fecha', 'hora')
        filename = f"lista_turnos_{hoy}.pdf"
    
    context = {
        'turnos': turnos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta
    }
    
    pdf = render_to_pdf('admin/pdf_turnos_lista.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error al generar el PDF", status=400)

@staff_member_required
def admin_usuarios(request):
    usuarios = User.objects.all().order_by('username')
    servicios = Servicio.objects.all()
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        action = request.POST.get('action')
        
        # Eliminar usuario
        if usuario_id and action == 'delete':
            usuario = get_object_or_404(User, pk=usuario_id)
            # No permitir eliminar al usuario actual
            if usuario != request.user:
                username = usuario.username
                usuario.delete()
                messages.success(request, f"El usuario {username} ha sido eliminado.")
            else:
                messages.error(request, "No puedes eliminar tu propio usuario.")
            return redirect('admin_usuarios')
        
        # Cambiar rol de usuario
        tipo = request.POST.get('tipo')
        servicio_id = request.POST.get('servicio')
        
        if usuario_id and tipo:
            usuario = get_object_or_404(User, pk=usuario_id)
            
            # Actualizar tipo de usuario
            if tipo == 'admin':
                usuario.is_staff = True
                usuario.save()
                # Si era profesional, eliminar ese rol
                if hasattr(usuario, 'profesional'):
                    usuario.profesional.delete()
            elif tipo == 'profesional':
                usuario.is_staff = False
                usuario.save()
                # Crear o actualizar profesional
                if servicio_id:
                    servicio = get_object_or_404(Servicio, pk=servicio_id)
                    if hasattr(usuario, 'profesional'):
                        usuario.profesional.servicio = servicio
                        usuario.profesional.save()
                    else:
                        Profesional.objects.create(user=usuario, servicio=servicio)
            else:  # cliente
                usuario.is_staff = False
                usuario.save()
                # Si era profesional, eliminar ese rol
                if hasattr(usuario, 'profesional'):
                    usuario.profesional.delete()
            
            messages.success(request, f"El rol de {usuario.username} ha sido actualizado.")
            return redirect('admin_usuarios')
    
    return render(request, 'admin/usuarios.html', {
        'usuarios': usuarios,
        'servicios': servicios,
        'active_tab': 'usuarios'
    })

@staff_member_required
def admin_consultas(request):
    consultas = Consulta.objects.all().order_by('-id')
    
    return render(request, 'admin/consultas.html', {
        'consultas': consultas,
        'active_tab': 'consultas'
    })

@staff_member_required
def admin_responder_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    
    if request.method == 'POST':
        asunto = request.POST.get('asunto', f"Re: Consulta Spa Bienestar")
        mensaje = request.POST.get('mensaje', '')
        
        # Codificar para URL
        asunto_encoded = quote(asunto)
        mensaje_encoded = quote(mensaje)
        
        # Crear URL de Gmail
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={consulta.email}&su={asunto_encoded}&body={mensaje_encoded}"
        
        # Redirigir al usuario a Gmail
        return redirect(gmail_url)
    
    return render(request, 'admin/responder_consulta.html', {
        'consulta': consulta,
        'active_tab': 'consultas'
    })

@staff_member_required
def admin_lista_turnos(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    turnos = Disponibilidad.objects.filter(servicio=servicio)
    return render(request, 'admin/servicio_turnos.html', {
        'servicio': servicio,
        'turnos': turnos,
        'active_tab': 'servicios'
    })

@staff_member_required
def admin_editar_turno(request, servicio_id=None, turno_id=None):
    if turno_id:
        turno = get_object_or_404(Disponibilidad, pk=turno_id)
        servicio_id = turno.servicio.id
    else:
        turno = Disponibilidad(servicio_id=servicio_id)

    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('admin_lista_turnos', servicio_id=servicio_id)
    else:
        form = DisponibilidadForm(instance=turno)

    return render(request, 'admin/editar_turno.html', {
        'form': form,
        'servicio_id': servicio_id,
        'nuevo': turno_id is None,
        'active_tab': 'servicios'
    })

@staff_member_required
def admin_eliminar_turno(request, turno_id):
    turno = get_object_or_404(Disponibilidad, pk=turno_id)
    servicio_id = turno.servicio.id
    turno.delete()
    return redirect('admin_lista_turnos', servicio_id=servicio_id)

@login_required
def pagar_turno(request, servicio_id, fecha_str, slot_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    slot = get_object_or_404(Disponibilidad, pk=slot_id)

    ahora = timezone.now()
    turno_datetime = datetime.combine(fecha, slot.hora_inicio)
    if timezone.is_naive(turno_datetime):
        turno_datetime = timezone.make_aware(turno_datetime)

    anticipado = turno_datetime - ahora >= timedelta(hours=48)
    precio_base = servicio.precio
    descuento = 0

    if request.method == 'POST':
        form = PagoForm(request.POST)
        metodo = request.POST.get('metodo_pago')
        if form.is_valid():
            if metodo == "debito" and anticipado:
                descuento = 0.15
                precio_final = int(precio_base * (1 - descuento))
            else:
                precio_final = precio_base

            cliente, _ = Cliente.objects.get_or_create(user=request.user)
            turno = Turno.objects.create(
                cliente=cliente,
                servicio=servicio,
                fecha=fecha,
                hora=slot.hora_inicio
            )

            send_mail(
                subject="Comprobante de pago - Spa Bienestar",
                message=(
                    f"¡Hola {request.user.get_full_name() or request.user.username}!\n\n"
                    f"Gracias por tu pago.\n\n"
                    f"🧖 Servicio: {servicio.nombre}\n"
                    f"📅 Fecha: {fecha.strftime('%d/%m/%Y')}\n"
                    f"🕐 Hora: {slot.hora_inicio.strftime('%H:%M')}\n"
                    f"💳 Monto pagado: ${precio_final:,}\n\n"
                    f"Te esperamos con gusto.\n"
                ),
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            messages.success(request, f"Tu pago de ${precio_final:,} fue procesado con éxito.")
            return redirect('reserva_exitosa', turno_id=turno.id)
    else:
        form = PagoForm()

    return render(request, 'pago.html', {
        'form': form,
        'servicio': servicio,
        'fecha': fecha,
        'slot': slot,
        'anticipado': anticipado,
        'precio_base': precio_base,
        'precio_descuento': int(precio_base * 0.85) if anticipado else None
    })

@login_required
def elegir_pago(request, servicio_id, fecha_str, slot_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    slot = get_object_or_404(Disponibilidad, pk=slot_id)
    fecha = parse_date(fecha_str)

    if request.method == 'POST':
        if request.POST.get('opcion') == 'consultorio':
            cliente, _ = Cliente.objects.get_or_create(user=request.user)
            turno = Turno.objects.create(
                cliente=cliente,
                servicio=servicio,
                fecha=fecha,
                hora=slot.hora_inicio
            )
            messages.success(request, "Tu turno ha sido reservado. Podés pagar en el consultorio.")
            return redirect('reserva_exitosa', turno_id=turno.id)
        elif request.POST.get('opcion') == 'online':
            return redirect('pagar_turno', servicio_id=servicio.id, fecha_str=fecha_str, slot_id=slot.id)

    return render(request, 'elegir_pago.html', {
        'servicio': servicio,
        'slot': slot,
        'fecha_str': fecha_str,
    })


def _get_cart(request):
    session_key = request.session.session_key or request.session.create()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
    else:
        cart = Cart.objects.filter(session_key=session_key).first()
        if not cart:
            cart = Cart.objects.create(session_key=session_key)
    return cart


def add_to_cart(request, servicio_id, fecha, hora):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    fecha_dt = timezone.datetime.strptime(fecha, '%Y-%m-%d').date()
    hora_dt  = timezone.datetime.strptime(hora,   '%H:%M').time()

    disp = servicio.disponibilidades.filter(
        fecha=fecha_dt, hora_inicio=hora_dt
    ).first()
    if not disp:
        messages.error(request, "Ese turno ya no está disponible.")
        return redirect('servicios')

    cart = _get_cart(request)
    CartItem.objects.get_or_create(
        cart     = cart,
        servicio = servicio,
        fecha    = fecha_dt,
        hora     = hora_dt,
        hora_fin = disp.hora_fin
    )

    return redirect(
        reverse(
            'reservar_por_fecha',
            args=[servicio_id, fecha_dt.year, fecha_dt.month, fecha_dt.day]
        )
    )


def view_cart(request):
    cart = _get_cart(request)
    items = cart.items.select_related('servicio').all()
    total = sum(item.servicio.precio for item in items)
    return render(request, 'cart.html', {
        'items': items,
        'total': total,
    })

@require_http_methods(["GET", "POST"])
def checkout(request):
    cart  = _get_cart(request)
    items = list(cart.items.select_related('servicio'))
    total = sum(item.servicio.precio for item in items)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para completar la reserva.")
            return redirect('login')

        try:
            cliente_obj = Cliente.objects.get(user=request.user)
        except Cliente.DoesNotExist:
            messages.error(request, "No pudimos encontrar tu perfil de Cliente.")
            return redirect('perfil')

        turnos_reservados = []
        for item in items:
            turno = Turno.objects.create(
                cliente  = cliente_obj,
                servicio = item.servicio,
                fecha    = item.fecha,
                hora     = item.hora
            )
            turnos_reservados.append(turno)

        cart.items.all().delete()
        return render(request, 'reserva_exitosa.html', {
            'turnos': turnos_reservados
        })

    hoy = timezone.now().date()
    if items:
        primer_dia = min(item.fecha for item in items)
        anticipado = (primer_dia - hoy) >= timedelta(days=2)
    else:
        anticipado = False

    precio_base      = total
    precio_descuento = round(total * 0.85, 2) if anticipado else total

    return render(request, 'pago.html', {
        'items':             items,
        'total':             total,
        'anticipado':        anticipado,
        'precio_base':       precio_base,
        'precio_descuento':  precio_descuento,
    })


def cart_remove(request, item_id):
    ci = get_object_or_404(CartItem, id=item_id)
    ci.delete()
    return redirect('view_cart')
