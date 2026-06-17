
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django.db.models import Q
from .models import Cliente, LineaServicio, Rubro, ColeccionRequestLog
from .serializers import ClienteSerializer, LineaServicioSerializer, RubroSerializer, ColeccionRequestLogSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [SearchFilter]
    search_fields = ['identificacion', 'razon_social']

    def get_queryset(self):
        return Cliente.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.delete()


class LineaServicioViewSet(viewsets.ModelViewSet):
    queryset = LineaServicio.objects.all()
    serializer_class = LineaServicioSerializer
    filter_backends = [SearchFilter]

    def get_queryset(self):
        queryset = LineaServicio.objects.filter(is_active=True)
        cliente_id = self.request.query_params.get('cliente_id')
        estado = self.request.query_params.get('estado')
        linea = self.request.query_params.get('linea')
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        if linea:
            queryset = queryset.filter(linea_numero=linea)
        return queryset

    def perform_destroy(self, instance):
        instance.delete()


class RubroViewSet(viewsets.ModelViewSet):
    queryset = Rubro.objects.all()
    serializer_class = RubroSerializer


class ColeccionRequestLogViewSet(viewsets.ModelViewSet):
    queryset = ColeccionRequestLog.objects.all()
    serializer_class = ColeccionRequestLogSerializer
