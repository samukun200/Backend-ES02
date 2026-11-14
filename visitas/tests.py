from datetime import time
from datetime import datetime, timezone as dt_timezone
from unittest.mock import Mock, patch

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

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


class VisitaApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='api-user',
            password='api-password',
        )

    def test_visitas_requiere_autenticacion(self):
        response = self.client.get(reverse('visita-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_puede_obtener_token_y_crear_visita(self):
        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'api-user', 'password': 'api-password'},
            format='json',
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}"
        )
        response = self.client.post(
            reverse('visita-list'),
            {
                'nombre': 'Persona de prueba',
                'rut': '12345678-5',
                'hora_entrada': '08:00:00',
                'motivo_visita': 'Reunión',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rut'], '12345678-5')

    def test_visita_rechaza_hora_de_salida_anterior(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('visita-list'),
            {
                'nombre': 'Persona de prueba',
                'rut': '12345678-5',
                'hora_entrada': '10:00:00',
                'hora_salida': '09:00:00',
                'motivo_visita': 'Reunión',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hora_salida', response.data)
