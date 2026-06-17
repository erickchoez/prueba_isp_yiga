
from django.contrib import admin
from .models import Cliente, LineaServicio, Rubro, ColeccionRequestLog

admin.site.register(Cliente)
admin.site.register(LineaServicio)
admin.site.register(Rubro)
admin.site.register(ColeccionRequestLog)
