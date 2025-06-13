from django.contrib import admin
from .models import CategoriaServicio, SubcategoriaServicio, Servicio, Cliente, Turno, Disponibilidad, Consulta

class DisponibilidadInline(admin.TabularInline):
    model = Disponibilidad
    extra = 1
    min_num = 0
    verbose_name = "Franja disponible"
    verbose_name_plural = "Franjas disponibles"

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [DisponibilidadInline]

@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    list_display   = ('servicio', 'fecha', 'hora_inicio', 'hora_fin')
    list_filter    = ('servicio', 'fecha')
    date_hierarchy = 'fecha'

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display  = ('cliente', 'servicio', 'fecha', 'hora')
    list_filter   = ('servicio', 'fecha')
    search_fields = ('cliente__nombre', 'servicio__nombre')

# Registra los modelos adicionales
@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(SubcategoriaServicio)
class SubcategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

from .models import Consulta, Subcategoria

class ConsultaAdmin(admin.ModelAdmin):
    # Simplemente muestra los campos que ya están en el modelo
    list_display = ['nombre', 'email', 'mensaje']  # Ajusta la lista de campos para mostrar en la vista admin

admin.site.register(Consulta, ConsultaAdmin)

from .models import Profesional

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('user', 'servicio')
    search_fields = ('user__username', 'user__email')