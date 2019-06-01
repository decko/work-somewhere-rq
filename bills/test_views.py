import pytest
from datetime import date

from django.urls import reverse

from rest_framework import status

pytestmark = pytest.mark.django_db


def test_telephone_bill_attributes_when_requesting_a_bill(client, bill):
    """
    Test for subscriber and period attributes in the response from
    Bills API detail endpoint.
    """

    attributes = {'subscriber', 'period'}
    url = reverse('bills:bill-detail', kwargs={'subscriber': 11111111111})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert attributes <= response.data.keys()


def test_detail_request_return_subscriber_number_on_response(client, bill):
    """
    Test for return of subscriber number when GETting a bill.
    """

    number = 11111111111
    url = reverse('bills:bill-detail', kwargs={'subscriber': number})

    response = client.get(url, content_type='application/json')

    assert response.data.get('subscriber') == str(number)


def test_detail_request_return_period_on_response(client, bill):
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


def test_period_return_when_using_month_abbreviation_on_url(client, bill):
    """
    Test for the return of the period when requested on the url using
    month 3 character abbreviation.
    """

    today = date.today()
    latest_period = today.replace(
        year=today.year if today.month > 2 else today.year - 1,
        month=today.month - 1 if today.month > 2 else 12,
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


def test_period_return_when_using_month_abbreviation_and_year_on_url(client, bill):
    """
    Test for the return of the period when requested on the url using
    month 3 character abbreviation and the year.
    """

    today = date.today()
    latest_period = today.replace(
        year=today.year if today.month > 2 else today.year - 1,
        month=today.month - 1 if today.month > 2 else 12,
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


def test_calls_attribute_when_request_a_bill(client, bill):
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

    assert len(response.data.get('calls', [])) == calls


@pytest.mark.parametrize('month_period, calls', (('Apr', 1), ('Dec', 0)))
def test_for_return_only_bills_of_a_given_month(client, bills, month_period, calls):
    """
    Test for return only bills of a given month without using year parameter.
    Since when no call was found returns a 404, using a empty list as
    default value for getting calls make the test pass without further changes.
    """

    url = reverse('bills:bill-detail', kwargs={'subscriber': '99988526423',
                                               'month_period': month_period})

    response = client.get(url)

    assert len(response.data.get('calls', [])) == calls


@pytest.mark.parametrize('month_period, year_period, calls', (
    ('Apr', 2019, 1), ('Dec', 2017, 6), ('Mar', 2018, 1)))
def test_for_return_only_bills_of_a_given_month_and_year(client, bills,
                                                         month_period,
                                                         year_period, calls):
    """
    Test for return only bills of a given month and year.
    """

    url = reverse('bills:bill-detail', kwargs={'subscriber': '99988526423',
                                               'month_period': month_period,
                                               'year_period': year_period})

    response = client.get(url)

    assert len(response.data.get('calls')) == calls


def test_for_return_404_when_no_call_is_found(client):
    """
    Test for return a 404 status code when no call was found for a
    given subscriber.
    """

    url = reverse('bills:bill-detail', kwargs={'subscriber': '33333333333'})

    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_for_using_current_month_as_url_parameter(client):
    """
    Test for using current month as URL parameter. Expect to raise
    a 400 Bad Request error if used the current month and current year.
    """

    current_month = date.today().strftime('%b')
    url = reverse('bills:bill-detail', kwargs={'subscriber': '99988526423',
                                               'month_period': current_month})

    response = client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
