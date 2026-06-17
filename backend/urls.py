
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ClienteViewSet, LineaServicioViewSet, RubroViewSet, ColeccionRequestLogViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'lineas', LineaServicioViewSet)
router.register(r'rubros', RubroViewSet)
router.register(r'logs', ColeccionRequestLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
