import pytest

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
