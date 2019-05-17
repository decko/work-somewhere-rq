from decimal import Decimal

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from calls.models import Call


class Bill(models.Model):
    call_duration = models.DurationField(_('Call Duration'))
    call_price = models.DecimalField(
        _('Call Price'),
        decimal_places=2,
        max_digits=14)
    call = models.ForeignKey('calls.Call', on_delete=models.SET_NULL)


@receiver(post_save, sender='calls.Call')
def bill_consolidated_call(sender, instance, **kwargs):
    """
    Get a instance of a consolidated Call, verify, bill it and
    inserts on the database.
    """

    if instance.start_timestamp and instance.stop_timestamp:
        call = Call.objects.get(pk=instance.pk)
        bill = Bill()
        bill.call = call
        bill.call_duration = call.stop_timestamp - call.start_timestamp
        bill.call_price = Decimal(10.00)
        bill.save()
