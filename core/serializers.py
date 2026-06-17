
from rest_framework import serializers
from .models import Cliente, LineaServicio, Rubro, ColeccionRequestLog


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class LineaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaServicio
        fields = '__all__'


class RubroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubro
        fields = '__all__'


class ColeccionRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColeccionRequestLog
        fields = '__all__'
