from datetime import time
from datetime import datetime, timezone as dt_timezone
from unittest.mock import Mock, patch

from django.contrib import messages
from django.test import TestCase, override_settings
from django.utils import timezone

from .admin import marcar_salida
from .models import Visita


class MarcarSalidaTests(TestCase):
    @override_settings(TIME_ZONE='America/Santiago')
    def test_marcar_salida_usa_la_hora_local_de_la_region_configurada(self):
        visita = Visita.objects.create(
            nombre='Persona de prueba',
            rut='12345678-9',
            hora_entrada=time(8, 0),
            motivo_visita='Prueba',
        )
        request = Mock()
        modeladmin = Mock()
        momento = datetime(2026, 10, 13, 15, 30, tzinfo=dt_timezone.utc)

        with timezone.override('America/Santiago'):
            with patch('visitas.admin.timezone.now', return_value=momento):
                marcar_salida(
                    modeladmin,
                    request,
                    Visita.objects.filter(pk=visita.pk),
                )

        visita.refresh_from_db()
        self.assertEqual(visita.hora_salida, time(12, 30))
        modeladmin.message_user.assert_called_once()
        self.assertEqual(modeladmin.message_user.call_args.args[2], messages.SUCCESS)
