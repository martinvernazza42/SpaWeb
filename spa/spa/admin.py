from django.contrib import admin
from .models import Servicio, Disponibilidad, Turno

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
