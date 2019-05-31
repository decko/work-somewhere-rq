import locale

from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.indexes import BrinIndex


class Bill(models.Model):
    source_call_url = models.URLField(_('Data source url'))
    subscriber = models.CharField(
        _('Call Source'),
        max_length=11,
        blank=True, null=True,
    )
    destination = models.CharField(
        _('Call Destination'),
        max_length=11,
        blank=True, null=True,
    )
    start_timestamp = models.DateTimeField(_('Start time of the call'))
    stop_timestamp = models.DateTimeField(_('Stop time of the call'))
    call_duration = models.DurationField(_('Call Duration'))
    call_price = models.DecimalField(
        _('Call Price'),
        decimal_places=2,
        max_digits=14)

    @property
    def call_start_date(self):
        return self.start_timestamp.date()

    @property
    def call_start_time(self):
        return self.start_timestamp.time()

    @property
    def call_price_rept(self):
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
        return locale.currency(self.call_price)

    @property
    def call_duration_formated(self):
        hours, minutes, seconds = str(self.call_duration).split(':')
        return f'{hours}h{minutes}m{seconds}s'

    def __repr__(self):
        return (f'subscriber: {self.subscriber} '
                f'destination: {self.destination} '
                f'call start date: {self.call_start_date}, '
                f'call start time: {self.call_start_time}, '
                f'call duration: {self.call_duration}, '
                f'call price: {self.call_price_rept}, '
                f'source call url: {self.source_call_url}')

    class Meta:
        indexes = [
            models.Index(fields=('subscriber',)),
            BrinIndex(fields=('stop_timestamp',)),
        ]
