import json
import pytest

from datetime import datetime
from decimal import Decimal

from core.services import ServiceAbstractClass

from .models import Bill
from .services import BillService

pytestmark = pytest.mark.django_db


def test_for_a_BillService_class():
    """
    Test for a BillService existence.
    """

    assert BillService


def test_for_a_BillService_as_a_ServiceAbstractClass_subclass():
    """
    Test for BillService as a ServiceAbstractClass subclass.
    """

    assert issubclass(BillService, ServiceAbstractClass)


def test_for_a_BillService_documentation():
    """
    Test for BillService documentation on class docstring.
    """

    assert BillService.__doc__


def test_for_BillService_trigger_and_queue_attributes():
    """
    Test for the values of trigger and queue attribute.
    """

    assert BillService.trigger == 'call-service-done'
    assert BillService.queue == 'bill-service-done'


def test_for_BillService_instance():
    """
    Test for a BillService instance.
    """

    instance = BillService()

    assert isinstance(instance, BillService)


def test_for_BillService_transformMessage_method(call):
    """
    Test for BillService transformMessage method to translate a message
    from CallService to a dict witch will be used to populate a Bill
    instance.

    Test uses call fixture.
    """

    message = json.dumps(call)

    instance = BillService(message=message)
    bill = instance.transformMessage()

    keys = {'subscriber', 'destination', 'start_timestamp', 'stop_timestamp',
            'call_duration', 'call_price', 'source_call_url'}

    assert keys == bill.keys()
    assert bill.get('subscriber') == call.get('source')
    assert bill.get('destination') == call.get('destination')


def test_for_transformMessage_dict_call_duration_value(call):
    """
    Test for BillService transformMessage method to translate a message
    from CallService to dict and expect call_duration value to be
    calculated and appended to dict.

    Test uses call fixture.
    """

    message = json.dumps(call)

    instance = BillService(message=message)
    bill = instance.transformMessage()

    start_timestamp = datetime.fromisoformat(call.get('start_timestamp'))
    stop_timestamp = datetime.fromisoformat(call.get('stop_timestamp'))
    call_duration = stop_timestamp - start_timestamp

    assert bill.get('call_duration') == call_duration


@pytest.mark.parametrize('std_charge_value', [None, 123])
def test_for_standing_charge_attribute(std_charge_value, mocker):
    """
    Test for standing_charge attribute be a Decimal type and setted
    at instanciation time.
    """

    mocker.patch.multiple(BillService, standing_charge=std_charge_value)

    with pytest.raises(AssertionError) as exception:
        instance = BillService()

    assert str(exception.value) == ('A standing_charge value must be a Decimal'
                                    ' type and set to make this'
                                    ' service work as expected.')

    mocker.resetall()


@pytest.mark.parametrize('call_charge_value', [None, 123])
def test_for_call_charge_attribute(call_charge_value, mocker):
    """
    Test for call_charge attribute be a Decimal type and setted
    at instanciation time.
    """

    mocker.patch.multiple(BillService, call_charge=None)

    with pytest.raises(AssertionError) as exception:
        instance = BillService()

    assert str(exception.value) == ('A call_charge value must be a Decimal'
                                    ' type and set to make this'
                                    ' service work as expected.')

    mocker.resetall()


def test_for_transformMessage_dict_call_price(call):
    """
    Test for BillService transformMessage method to translate a message
    from CallService to dict and expect call_price value to be
    calculated and appended to dict.

    Test uses call fixture.
    """

    message = json.dumps(call)

    instance = BillService(message=message)
    bill = instance.transformMessage()

    call_duration = bill.get('call_duration')

    std_charge = Decimal('0.36')
    call_charge = Decimal('0.09')
    minutes_call_duration = call_duration.seconds // 60

    call_price = std_charge + (minutes_call_duration * call_charge)

    assert bill.get('call_price') == call_price


@pytest.mark.parametrize('start_call, stop_call, call_price', [
    ((2019, 4, 26, 21, 57, 13), (2019, 4, 26, 22, 17, 13), Decimal('0.54')),
    ((2017, 12, 11, 15, 7, 13), (2017, 12, 12, 22, 50, 56), Decimal('123.75')),
    ((2017, 12, 12, 22, 47, 56), (2017, 12, 12, 22, 50, 56), Decimal('125.64')),
    ((2017, 12, 12, 21, 57, 13), (2017, 12, 12, 22, 10, 56), Decimal('0.54')),
    ((2017, 12, 12, 4, 57, 13), (2017, 12, 12, 6, 10, 56), Decimal('1.17')),
    ((2017, 12, 13, 21, 57, 13), (2017, 12, 14, 22, 10, 56), Decimal('86.85')),
    ((2017, 12, 12, 15, 7, 58), (2017, 12, 12, 15, 12, 56), Decimal('0.72')),
    ((2018, 2, 28, 21, 57, 13), (2018, 3, 1, 22, 10, 56), Decimal('86.85')),
])
def test_for_transformMessage_dict_call_price_at_reduced_tariff_time(call,
                                                                     start_call,
                                                                     stop_call,
                                                                     call_price):
    """
    Test for BillService transformMessage method to translate a message
    from CallService to dict and expect call_price value to be
    calculated at reduced tariff time and appended to dict.

    Test uses call fixture.
    """
    start_timestamp = datetime(*start_call)
    stop_timestamp = datetime(*stop_call)

    call['start_timestamp'] = start_timestamp.isoformat()
    call['stop_timestamp'] = stop_timestamp.isoformat()

    message = json.dumps(call)

    instance = BillService(message=message)
    bill = instance.transformMessage()

    assert bill.get('call_price') == call_price


def test_for_BillService_persistData_return_a_Bill_instance(call):
    """
    Test for BillService persistData to return a Bill model instance.

    Test uses call fixture.
    """

    message = json.dumps(call)

    instance = BillService(message=message)
    instance.transformMessage()

    instance.persistData()

    assert isinstance(instance.persisted_data, Bill)


def test_for_persistData_raise_an_AssertionError():
    """
    Test for persistData raise an AssertionError if self.data is None
    or not an instance of dict.
    """

    instance = BillService()

    with pytest.raises(AssertionError) as exception:
        instance.data = None
        instance.persistData()

    assert exception
