import re

from rest_framework import serializers

from .models import Registry
from .models import Call


def validate_number(value):
    """
    Check if the 'source' value is a valid brazillian phone number.
    """

    expression = r'(^[1-9]\d)(\d{8,10})'
    match = re.match(expression, value)

    if not match:
        raise serializers.ValidationError(
            "The number is not a valid phone number")

    return value


class RegistrySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to validate registry data. source and destination
    are validated against a phone number validator.
    """

    source = serializers.CharField(
        required=False, validators=(validate_number,))

    destination = serializers.CharField(
        required=False, validators=(validate_number,))

    class Meta:
        model = Registry
        fields = ('url', 'id', 'type', 'timestamp', 'call_id', 'source',
                  'destination')
        extra_kwargs = {
            'url': {'view_name': 'calls:registry-detail'}
        }


class CallSerializer(serializers.ModelSerializer):
    """
    Serializer to validate and serialize Call instances
    """

    class Meta:
        model = Call
        fields = ('call_id', 'start_timestamp', 'stop_timestamp', 'source',
                  'destination')
