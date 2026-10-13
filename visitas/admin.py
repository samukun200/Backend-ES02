from django.contrib import admin
from django.contrib import messages
from django.utils import timezone

from .models import Visita


@admin.action(description='Marcar salida (hora actual)')
def marcar_salida(modeladmin, request, queryset):
    hora_salida = timezone.localtime().time().replace(microsecond=0)
    visitas_pendientes = queryset.filter(hora_salida__isnull=True)
    cantidad_actualizada = visitas_pendientes.update(hora_salida=hora_salida)
    cantidad_omitida = queryset.count() - cantidad_actualizada

    if cantidad_actualizada:
        modeladmin.message_user(
            request,
            f'{cantidad_actualizada} visita(s) marcada(s) con salida a las '
            f'{hora_salida.strftime("%H:%M")}.',
            messages.SUCCESS,
        )
    if cantidad_omitida:
        modeladmin.message_user(
            request,
            f'{cantidad_omitida} visita(s) ya tenía(n) una hora de salida y no fue(ron) modificada(s).',
            messages.WARNING,
        )


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
    list_filter = ('fecha_registro',)
    search_fields = ('nombre', 'rut', 'motivo_visita')
    ordering = ('-fecha_registro', '-hora_entrada')
    actions = (marcar_salida,)
