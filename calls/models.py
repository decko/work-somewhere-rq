from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .managers import ConsolidatedCallManager


class Registry(models.Model):
    type = models.CharField(
        _('Call type'),
        choices=(('start', 'Start'), ('stop', 'Stop')),
        max_length=5,
    )
    timestamp = models.DateTimeField(
        _('Timestamp of the call'),
    )
    call_id = models.IntegerField(
        _('Unique call pair identifier'),
    )
    source = models.CharField(
        _('Call Source'),
        max_length=11,
        blank=True, null=True,
    )
    destination = models.CharField(
        _('Call Destination'),
        max_length=11,
        blank=True, null=True,
    )

    def get_absolute_url(self):
        return reverse_lazy('calls:registry-detail',
                            kwargs={'pk': self.id})

    def __str__(self):
        if type == 'start':
            return (f'call type: {self.type}, when: {self.timestamp}, '
                    'call id: {self.call_id}, source: {self.source}, '
                    'destination: {self.destination}')

        return f'call type: {self.type},\
                when: {self.timestamp},\
                call id: {self.call_id}'


class Call(models.Model):
    call_id = models.IntegerField(
        _('Unique call identifier'),
        unique=True
    )
    start_timestamp = models.DateTimeField(
        _('Start time of the call'),
        blank=True,
        null=True
    )
    stop_timestamp = models.DateTimeField(
        _('Stop time of the call'),
        blank=True,
        null=True
    )
    source = models.CharField(
        _('Call Source'),
        max_length=11,
        blank=True, null=True,
    )
    destination = models.CharField(
        _('Call Destination'),
        max_length=11,
        blank=True, null=True,
    )

    objects = models.Manager()
    consolidated = ConsolidatedCallManager()

    def get_absolute_url(self):
        return reverse_lazy('calls:call-detail',
                            kwargs={'call_id': self.call_id})
