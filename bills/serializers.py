from rest_framework import serializers
from rest_framework.generics import ListAPIView

from .models import Bill


class BilledCallSerializer(serializers.ModelSerializer):
    destination = serializers.CharField(source='call.destination')
    call_start_date = serializers.SerializerMethodField()
    call_start_time = serializers.SerializerMethodField()
    call_duration = serializers.DurationField()
    call_price = serializers.DecimalField(max_digits=14, decimal_places=2)

    def get_call_start_date(self, obj):
        return obj.call.start_timestamp.date()

    def get_call_start_time(self, obj):
        return obj.call.start_timestamp.time()

    class Meta:
        model = Bill
        fields = ('destination', 'call_start_date', 'call_start_time',
                 'call_duration', 'call_price')
