import pytest

pytestmark = pytest.mark.django_db


def test_for_Bill_call_start_date_property(bill):
    """
    Test for call_start_date property on a Bill instance.
    """

    date = bill.start_timestamp.date()
    assert bill.call_start_date == date


def test_for_Bill_call_start_time_property(bill):
    """
    Test for call_start_time property on a Bill instance.
    """

    time = bill.start_timestamp.time()
    assert bill.call_start_time == time


def test_for_Bill_call_price_rept(bill):
    """
    Test for call_price_rept property on a Bill instance, which contains
    call_price represented in Brazillian Real (R$).
    """

    call_price = f"R$ {str(bill.call_price).replace('.', ',')}"
    assert bill.call_price_rept == call_price
