from django.db import models
from django.utils import timezone

class Visita(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=10)
    fecha_registro = models.DateField(default=timezone.localdate, editable=False)
     # Ingresar la hora con el formato HH:MM:SS, por ejemplo: 14:30:00.
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(
        null=True,
        blank=True,
        help_text='Déjalo vacío si la persona aún no ha salido.',
    )

    motivo_visita = models.TextField(max_length=100)
