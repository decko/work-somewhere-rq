from rest_framework import serializers

from .models import Registry
from .models import Call


class RegistrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Registry
        fields = ('id', 'type', 'timestamp', 'call_id', 'source',
                  'destination')


class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        fields = ('call_id', 'start_timestamp', 'stop_timestamp', 'source',
                  'destination')
