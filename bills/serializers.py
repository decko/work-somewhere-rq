from rest_framework import serializers
from rest_framework.generics import ListAPIView

from .models import Bill


class BilledCallSerializer(serializers.ModelSerializer):
    destination = serializers.CharField()
    call_start_date = serializers.DateField()
    call_start_time = serializers.TimeField()
    call_duration = serializers.DurationField()
    call_price = serializers.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = Bill
        fields = ('destination', 'call_start_date', 'call_start_time',
                  'call_duration', 'call_price')
