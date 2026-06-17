
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import LineaServicio, Rubro, ColeccionRequestLog


@shared_task
def check_morosidad():
    now = timezone.now()
    lineas = LineaServicio.objects.filter(is_active=True).select_related('cliente').prefetch_related('rubros')

    for linea in lineas:
        log = ColeccionRequestLog.objects.create(
            linea_servicio=linea,
            started_at=now,
            status='SUCCESS',
            unpaid_count=0,
            action_taken='NONE'
        )

        try:
            with transaction.atomic():
                if linea.estado in ['CANCELADO', 'NO_INSTALADO']:
                    log.finished_at = timezone.now()
                    log.save()
                    continue

                # Obtener rubros vencidos y no pagados
                rubros_vencidos = linea.rubros.filter(
                    estado__in=['NO_PAGADO', 'VENCIDO'],
                    fecha_vencimiento__lt=now
                ).select_for_update()

                unpaid_count = rubros_vencidos.count()
                saldo_vencido = sum(r.valor_total for r in rubros_vencidos)

                log.unpaid_count = unpaid_count
                log.saldo_vencido = saldo_vencido
                linea.saldo_vencido = saldo_vencido

                if unpaid_count > 0:
                    if linea.estado != 'SUSPENDIDO':
                        linea.estado = 'SUSPENDIDO'
                        log.action_taken = 'SUSPEND'
                else:
                    if linea.estado == 'SUSPENDIDO':
                        linea.estado = 'ACTIVO'
                        log.action_taken = 'UNSUSPEND'

                linea.save()
                log.finished_at = timezone.now()
                log.status = 'SUCCESS'
                log.save()

        except Exception as e:
            log.finished_at = timezone.now()
            log.status = 'FAILED'
            log.error_message = str(e)
            log.save()
