import calendar
from datetime import datetime, timedelta, date as _date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.dateparse import parse_date
from django.core.mail import send_mail 


from .forms import CustomAuthForm
from .forms import RegistroUsuarioForm, ConsultaForm, DisponibilidadForm
from .forms import PagoForm
from .models import SubcategoriaServicio, Servicio, Disponibilidad, Turno, Cliente, Consulta

# -------------------------------------------------------------------
# Vistas Públicas
# -------------------------------------------------------------------

def index(request):
    return render(request, 'index.html')


def servicios(request):
    # Capturamos el filtro de subcategoría (categoría)
    subcategoria_id = request.GET.get('subcategoria')

    if subcategoria_id:
        # Objeto de la categoría seleccionada
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

    # Año/mes del querystring (o hoy)
    try:
        year = int(request.GET.get('year', hoy.year))
    except ValueError:
        year = hoy.year
    try:
        month = int(request.GET.get('month', hoy.month))
    except ValueError:
        month = hoy.month

    # Cálculo de mes anterior / siguiente
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

    # Traigo todas las disponibilidades del mes...
    qs = Disponibilidad.objects.filter(
        servicio=servicio,
        fecha__year=year,
        fecha__month=month
    )

    # Filtrar slots libres y a más de 48 horas
    disponibles = []
    cutoff = ahora + timedelta(hours=48)
    for d in qs:
        slot_dt = datetime.combine(d.fecha, d.hora_inicio)
        # Aware datetime si es naive
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

    # Construyo el set de días que todavía están libres
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

    # 🔽 Traer todas las disponibilidades para ese día
    todos_los_slots = Disponibilidad.objects.filter(servicio=servicio, fecha=fecha_obj)

    # 🔽 Filtrar SOLO los que no están tomados
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


def mis_turnos(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    turnos = Turno.objects.filter(cliente=cliente).order_by('fecha', 'hora')
    return render(request, 'mis_turnos.html', {'turnos': turnos})


@staff_member_required
def admin_lista_turnos(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    turnos = Disponibilidad.objects.filter(servicio=servicio)
    return render(request, 'admin/servicio_turnos.html', {
        'servicio': servicio,
        'turnos': turnos
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
        'nuevo': turno_id is None
    })


@staff_member_required
def admin_eliminar_turno(request, turno_id):
    turno = get_object_or_404(Disponibilidad, pk=turno_id)
    servicio_id = turno.servicio.id
    turno.delete()
    return redirect('admin_lista_turnos', servicio_id=servicio_id)



from datetime import timedelta, datetime
from django.utils import timezone

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
        print("POST data:", request.POST)
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

            # ✅ Enviar mail (a consola en DEBUG)
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
            print("Errores del formulario:", form.errors)
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