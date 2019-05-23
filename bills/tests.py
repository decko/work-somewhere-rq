import pytest
from datetime import date

from django.urls import resolve, reverse
from rest_framework import status

from calls.tests import start_call_fx, stop_call_fx

from core.services import ServiceAbstractClass

from .services import BillService
pytestmark = pytest.mark.django_db


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


def test_call_instance_attribute_on_a_bill(client):
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


def test_attribute_values_given_a_consolidated_call(client, start_call_fx, stop_call_fx):
    """
    Test for GETting a Bill from a subscriber number given a consolidated call.

    Test uses start_call_fx fixture.
    Test uses stop_call_fx fixture.
    """

    registry_url = reverse('calls:registry-list')
    data = [start_call_fx, stop_call_fx]

    for registry in data:
        response = client.post(registry_url, registry, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    bill_url = reverse('bills:bill-detail',
                       kwargs={'subscriber': start_call_fx.get('source')})

    response = client.get(bill_url)

    assert len(response.data.get('calls')) == 1

    call = response.data.get('calls')[0]

    assert call.get('destination') == start_call_fx.get('destination')


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
