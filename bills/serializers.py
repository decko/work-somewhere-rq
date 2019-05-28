from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Bill


class BilledCallSerializer(serializers.ModelSerializer):
    """
    Serializes a billed call.
    """
    destination = serializers.CharField()
    call_start_date = serializers.DateField()
    call_start_time = serializers.TimeField()
    call_duration = serializers.CharField(source='call_duration_formated')
    call_price = serializers.CharField(source='call_price_rept')

    class Meta:
        model = Bill
        fields = ('destination', 'call_start_date', 'call_start_time',
                  'call_duration', 'call_price')


class BillSerializer(serializers.Serializer):
    """
    Serializes a bill. It contains the subscriber number,
    a period (month/year) and a list of calls.
    """

    subscriber = serializers.CharField(label=_('Subscriber Telephone Number'))
    period = serializers.CharField(label=_('Reference Period'))
    calls = BilledCallSerializer(label=_('Call Records'), many=True)
