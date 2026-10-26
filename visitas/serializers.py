from rest_framework import serializers

from .models import Visita

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = '__all__'