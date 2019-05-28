import pytest

from rest_framework.serializers import ModelSerializer

from .models import Bill

from .serializers import BillSerializer
from .serializers import BilledCallSerializer

pytestmark = pytest.mark.django_db


def test_for_call_duration_value_format(bill):
    """
    Test for call_duration value format. e.g. 0h35m42s
    """

    serializer = BilledCallSerializer(bill)

    call_duration = serializer.data.get('call_duration')

    formated_time = '0h08m00s'

    assert call_duration == formated_time


def test_for_call_price_value_format(bill):
    """
    Test for call_price value formated. e.g. R$ 3,96
    """

    serializer = BilledCallSerializer(bill)

    call_price = serializer.data.get('call_price')

    call_price_formated = 'R$ 1,08'

    assert call_price == call_price_formated


def test_for_a_BillSerializer():
    """
    Test for a BillSerializer existence.
    """

    assert BillSerializer


def test_for_BillSerializer_to_inherit_from_ModelSerializer():
    """
    Test for BillSerializer be a ModelSerializer subclass.
    """

    assert issubclass(BillSerializer, ModelSerializer)


def test_for_Meta_property_with_model_attribute():
    """
    Test for Meta property with model attribute setted to Bill model.
    """

    assert BillSerializer.Meta.model == Bill


def test_for_BillSerializer_documentation():
    """
    Test for BillSerializer documentation on class docstring.
    """

    assert BillSerializer.__doc__


def test_for_BillSerializer_fields():
    """
    Test for subscriber, period attributes and a list of calls.
    """

    serializer = BillSerializer()

    fields = {'subscriber', 'period', 'calls'}

    assert fields <= serializer.get_fields().keys()
