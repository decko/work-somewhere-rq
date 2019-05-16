from django.urls import resolve, reverse
from rest_framework import status


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
    assert attributes >= response.data
