import calendar
from datetime import date as _date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, logout
from django.contrib.admin.views.decorators import staff_member_required

from .forms import RegistroUsuarioForm, ConsultaForm, DisponibilidadForm
from .models import (
    CategoriaServicio, Subcategoria, SubcategoriaServicio,
    Servicio, Disponibilidad, Turno, Cliente, Consulta
)


def index(request):
    return render(request, 'index.html')

def servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios.html', {'servicios': servicios})

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def consultas(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'consultas.html', {
                'form': form,
                'mensaje': 'Consulta enviada exitosamente!'
            })
    else:
        form = ConsultaForm()
    return render(request, 'consultas.html', {'form': form})

def turnos(request):
    return render(request, 'turnos.html')

def calendario_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    hoy   = _date.today()
    year  = int(request.GET.get('year',  hoy.year))
    month = int(request.GET.get('month', hoy.month))

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)

    qs = Disponibilidad.objects.filter(
        servicio=servicio,
        fecha__year=year,
        fecha__month=month
    )
    available = {d.fecha.day for d in qs}
    day_names = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']

    return render(request, 'calendario_servicio.html', {
        'servicio':   servicio,
        'year':       year,
        'month':      month,
        'month_days': month_days,
        'available':  available,
        'day_names':  day_names,
    })

def reservar_por_fecha(request, servicio_id, year, month, day):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    fecha_obj = _date(year, month, day)
    slots = Disponibilidad.objects.filter(servicio=servicio, fecha=fecha_obj)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para reservar un turno.')
            return redirect(f"{auth_views.LoginView.login_url}?next={request.path}")

        cliente, _ = Cliente.objects.get_or_create(user=request.user)
        slot_id = request.POST.get('slot_id')
        slot = get_object_or_404(Disponibilidad, pk=slot_id)

        turno = Turno.objects.create(
            cliente  = cliente,
            servicio = servicio,
            fecha    = fecha_obj,
            hora     = slot.hora_inicio
        )
        return redirect('reserva_exitosa', turno_id=turno.id)

    return render(request, 'reservar_por_fecha.html', {
        'servicio': servicio,
        'day':       fecha_obj,
        'slots':     slots,
    })

@login_required
def reserva_exitosa(request, turno_id):
    turno = get_object_or_404(
        Turno,
        pk=turno_id,
        cliente__user=request.user
    )
    return render(request, 'reserva_exitosa.html', {
        'turno': turno
    })

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

# *** logout_view que acepta GET y redirige a login ***
from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# Login usando la vista genérica
login_view = auth_views.LoginView.as_view(template_name='login.html')

@login_required
def perfil(request):
    turnos = Turno.objects.filter(cliente=request.user.cliente)
    consultas = Consulta.objects.filter(email=request.user.email)
    return render(request, 'perfil.html', {
        'turnos':    turnos,
        'consultas': consultas
    })

@login_required
def mis_turnos(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    turnos = Turno.objects.filter(cliente=cliente).order_by('fecha', 'hora')
    return render(request, 'mis_turnos.html', {
        'turnos': turnos
    })

# -------------------------------------------------------------------
# Vistas de administración para gestión de turnos
# -------------------------------------------------------------------

@staff_member_required
def admin_lista_turnos(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    turnos = Disponibilidad.objects.filter(servicio=servicio)
    return render(request, 'admin/servicio_turnos.html', {
        'servicio': servicio,
        'turnos':    turnos
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
        'form':        form,
        'servicio_id': servicio_id,
        'nuevo':       turno_id is None
    })

@staff_member_required
def admin_eliminar_turno(request, turno_id):
    turno = get_object_or_404(Disponibilidad, pk=turno_id)
    servicio_id = turno.servicio.id
    turno.delete()
    return redirect('admin_lista_turnos', servicio_id=servicio_id)
