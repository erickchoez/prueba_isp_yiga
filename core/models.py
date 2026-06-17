
from django.db import models
from django.utils import timezone


class AuditDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cliente(AuditDateModel):
    identificacion = models.CharField(max_length=20, unique=True, db_index=True)
    razon_social = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class LineaServicio(AuditDateModel):
    ESTADOS = [
        ('NO_INSTALADO', 'NO_INSTALADO'),
        ('ACTIVO', 'ACTIVO'),
        ('SUSPENDIDO', 'SUSPENDIDO'),
        ('CANCELADO', 'CANCELADO'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='lineas')
    linea_numero = models.PositiveSmallIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='NO_INSTALADO')
    fecha_instalacion = models.DateField(null=True, blank=True)
    saldo_vencido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('cliente', 'linea_numero')

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.linea_numero < 1:
            raise ValidationError('linea_numero debe ser >= 1')
        if not self.cliente.is_active and self.estado == 'ACTIVO':
            raise ValidationError('No se puede activar una línea de un cliente inactivo')


class Rubro(AuditDateModel):
    ESTADOS = [
        ('NO_PAGADO', 'NO_PAGADO'),
        ('PAGADO', 'PAGADO'),
        ('VENCIDO', 'VENCIDO'),
        ('ANULADO', 'ANULADO'),
    ]

    linea_servicio = models.ForeignKey(LineaServicio, on_delete=models.CASCADE, related_name='rubros')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='NO_PAGADO')
    fecha_emision = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField()
    fecha_pago = models.DateTimeField(null=True, blank=True)


class ColeccionRequestLog(AuditDateModel):
    STATUS = [
        ('SUCCESS', 'SUCCESS'),
        ('FAILED', 'FAILED'),
    ]

    ACTIONS = [
        ('NONE', 'NONE'),
        ('SUSPEND', 'SUSPEND'),
        ('UNSUSPEND', 'UNSUSPEND'),
    ]

    linea_servicio = models.ForeignKey(LineaServicio, on_delete=models.CASCADE, related_name='logs')
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS)
    unpaid_count = models.PositiveSmallIntegerField()
    action_taken = models.CharField(max_length=20, choices=ACTIONS, default='NONE')
    error_message = models.TextField(null=True, blank=True)
