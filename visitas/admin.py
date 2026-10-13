from django.contrib import admin

from .models import Visita


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'rut',
        'fecha_registro',
        'hora_entrada',
        'hora_salida',
        'motivo_visita',
    )
    list_editable = ('hora_salida',)
    list_filter = ('fecha_registro', 'rut')
    search_fields = ('nombre', 'rut', 'motivo_visita')
    ordering = ('-fecha_registro', '-hora_entrada')
