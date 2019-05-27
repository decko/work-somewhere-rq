import json
import pytest
from datetime import date
from datetime import datetime
from decimal import Decimal

from django.urls import resolve, reverse
from rest_framework import status

from model_mommy import mommy

from calls.tests import start_call_fx, stop_call_fx

from core.services import ServiceAbstractClass

from .models import Bill
from .services import BillService

pytestmark = pytest.mark.django_db


@pytest.fixture(scope="session")
def bills(django_db_setup, django_db_blocker):
    source = '99988526423'
    destination = '9933468278'

    calls = (
        (70, datetime(2019, 4, 26, 21, 57, 13), datetime(2019, 4, 26, 22, 17, 13), Decimal('0.54')),
        (71, datetime(2017, 12, 11, 15, 7, 13), datetime(2017, 12, 12, 22, 50, 56), Decimal('123.75')),
        (72, datetime(2017, 12, 12, 22, 47, 56), datetime(2017, 12, 12, 22, 50, 56), Decimal('125.64')),
        (73, datetime(2017, 12, 12, 21, 57, 13), datetime(2017, 12, 12, 22, 10, 56), Decimal('0.54')),
        (74, datetime(2017, 12, 12, 4, 57, 13), datetime(2017, 12, 12, 6, 10, 56), Decimal('1.17')),
        (75, datetime(2017, 12, 13, 21, 57, 13), datetime(2017, 12, 14, 22, 10, 56), Decimal('86.85')),
        (76, datetime(2017, 12, 12, 15, 7, 58), datetime(2017, 12, 12, 15, 12, 56), Decimal('0.72')),
        (77, datetime(2018, 2, 28, 21, 57, 13), datetime(2018, 3, 1, 22, 10, 56), Decimal('86.85')),
    )

    with django_db_blocker.unblock():
        for call in calls:
            mommy.make(Bill,
                       source_call_url=f"/api/v1/calls/{call[0]}",
                       subscriber=source,
                       destination=destination,
                       start_timestamp=call[1],
                       stop_timestamp=call[2],
                       call_duration=call[2]-call[1],
                       call_price=call[3])

    bills = Bill.objects.all()

    yield bills

    with django_db_blocker.unblock():
        for bill in bills:
            bill.delete()


@pytest.fixture
def call():
    """
    Fixture containing a dict with the result of a successful CallService
    processing.
    """

    call = {'url': '/calls/1',
            'call_id': 1,
            'start_timestamp': '2019-04-26T12:32:10',
            'stop_timestamp': '2019-04-26T12:40:10',
            'source': '11111111111',
            'destination': '22222222222'}

    return call


@pytest.fixture
def bill(call):
    """
    Fixture that insert a Bill instance and delete it when test is done.
    """

    message = json.dumps(call)

    instance = BillService(message=message)
    instance.transformMessage()
    instance.persistData()

    yield instance.persisted_data

    instance.persisted_data.delete()


def test_list_bills_api_endpoint_return_403(client):
    """
    Test for GETting the Bills List API Endpoint and expect it
    to return 403 since it's no one is authorized to get a list
    from it.
    """

    url = '/api/v1/bills'

    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_namespace_of_bills_api_list_endpoint():
    """
    Test if there is a Bills API list endpoint and is defined as "bills"
    namespace and "bill-list" as his name.
    """

    url = '/api/v1/bills'
    resolved = resolve(url)

    assert resolved.namespace == 'bills'\
        and resolved.url_name == 'bill-list'


def test_reverse_namespace_for_bills_api_detail_endpoint():
    """
    Test for reverse a Bills API Detail endpoint using name and
    namespace and using subscriber parameter as identifier.
    """

    view_name = 'bills:bill-detail'
    reversed = reverse(view_name, kwargs={'subscriber': 11111111111})

    assert reversed == '/api/v1/bills/11111111111'


def test_telephone_bill_attributes_when_requesting_a_bill(client):
    """
    Test for subscriber and period attributes in the response from
    Bills API detail endpoint.
    """

    attributes = {'subscriber', 'period'}
    url = reverse('bills:bill-detail', kwargs={'subscriber': 11111111111})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert attributes <= response.data.keys()


def test_detail_request_return_subscriber_number_on_response(client):
    """
    Test for return of subscriber number when GETting a bill.
    """

    number = 11111111111
    url = reverse('bills:bill-detail', kwargs={'subscriber': number})

    response = client.get(url, content_type='application/json')

    assert response.data.get('subscriber') == number


def test_detail_request_return_period_on_response(client):
    """
    Test for return of the latest period on the request to Bill API
    detail endpoint.
    """

    number = 11111111111
    url = reverse('bills:bill-detail', kwargs={'subscriber': number})

    today = date.today()
    latest_period = today.replace(
        year=today.year if today.month > 1 else today.year - 1,
        month=today.month - 1 if today.month > 1 else 12,
        day=1).strftime('%h/%Y')

    response = client.get(url, content_type='application/json')

    assert response.data.get('period') == latest_period


def test_period_return_when_using_month_abbreviation_on_url(client):
    """
    Test for the return of the period when requested on the url using
    month 3 character abbreviation.
    """

    today = date.today()
    latest_period = today.replace(
        year=today.year if today.month > 2 else today.year - 1,
        month=today.month - 2 if today.month > 2 else 12,
        day=1)
    month = latest_period.strftime('%h')
    month_year = latest_period.strftime('%h/%Y')

    number = 11111111111
    url = reverse('bills:bill-detail', kwargs={
        'subscriber': number,
        'month_period': month
    })

    response = client.get(url)

    assert response.data.get('period') == month_year


def test_period_return_when_using_month_abbreviation_and_year_on_url(client):
    """
    Test for the return of the period when requested on the url using
    month 3 character abbreviation and the year.
    """

    today = date.today()
    latest_period = today.replace(
        year=today.year if today.month > 2 else today.year - 1,
        month=today.month - 2 if today.month > 2 else 12,
        day=1)
    month_period = latest_period.strftime('%h')
    year_period = latest_period.strftime('%Y')

    number = 11111111111
    url = reverse('bills:bill-detail', kwargs={
        'subscriber': number,
        'month_period': month_period,
        'year_period': year_period
    })

    response = client.get(url)

    assert response.data.get('period') == f"{month_period}/{year_period}"


def test_calls_attribute_when_request_a_bill(client):
    """
    Test for calls attribute in the response from Bills API Endpoint.
    Expect it to be a list.
    """

    number = 11111111111
    url = reverse('bills:bill-detail', kwargs={'subscriber': number})

    response = client.get(url)

    assert isinstance(response.data.get('calls'), list)


def test_call_instance_attribute_on_a_bill(client, bill):
    """
    Test for a list of attributes for each call in the list of a bill.
    Expect to find 'destination', 'call_start_date', 'call_start_time',
    'call_duration', 'call_price'.
    """

    attributes = {'destination', 'call_start_date', 'call_start_time',
                  'call_duration', 'call_price'}

    number = 11111111111
    url = reverse('bills:bill-detail', kwargs={'subscriber': number})

    response = client.get(url)

    call = response.data.get('calls')[0]

    assert attributes <= call.keys()


@pytest.mark.parametrize('subscriber, calls', [
    ('11111111111', 1), ('99988526423', 0)
])
def test_for_get_a_bill_from_a_subscriber_number_given_a_consolidated_call(client, bill,
                                                                           subscriber,
                                                                           calls):
    """
    Test for GETting a Bill from a subscriber number given a consolidated call.
    """

    bill_url = reverse('bills:bill-detail',
                       kwargs={'subscriber': subscriber})

    response = client.get(bill_url)

    assert len(response.data.get('calls')) == calls


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
