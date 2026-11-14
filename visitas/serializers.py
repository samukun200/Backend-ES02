import re

from rest_framework import serializers

from .models import Visita


class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = (
            'id',
            'nombre',
            'rut',
            'fecha_registro',
            'hora_entrada',
            'hora_salida',
            'motivo_visita',
        )
        read_only_fields = ('id', 'fecha_registro')

    def validate_nombre(self, value):
        value = ' '.join(value.split())
        if not value:
            raise serializers.ValidationError(
                'Ingresa el nombre del visitante.'
            )
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü .'-]+", value):
            raise serializers.ValidationError(
                'El nombre solo puede contener letras y espacios.'
            )
        return value

    def validate_rut(self, value):
        value = value.strip().replace('.', '').replace(' ', '').upper()
        if not re.fullmatch(r'\d{7,8}-[0-9K]', value):
            raise serializers.ValidationError(
                'Ingresa el RUT con formato 12345678-5.'
            )

        cuerpo, digito = value.split('-')
        suma = 0
        multiplicador = 2
        for numero in reversed(cuerpo):
            suma += int(numero) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)
        digito_valido = (
            '0' if resto == 11 else 'K' if resto == 10 else str(resto)
        )
        if digito != digito_valido:
            raise serializers.ValidationError(
                'El dígito verificador del RUT no es válido.'
            )
        return value

    def validate_motivo_visita(self, value):
        value = ' '.join(value.split())
        if not value:
            raise serializers.ValidationError(
                'Ingresa el motivo de la visita.'
            )
        return value

    def validate(self, attrs):
        hora_entrada = attrs.get(
            'hora_entrada',
            getattr(self.instance, 'hora_entrada', None),
        )
        hora_salida = attrs.get(
            'hora_salida',
            getattr(self.instance, 'hora_salida', None),
        )
        if hora_entrada and hora_salida and hora_salida <= hora_entrada:
            raise serializers.ValidationError({
                'hora_salida': (
                    'La hora de salida debe ser posterior a la hora de entrada.'
                ),
            })
        return attrs
