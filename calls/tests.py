from datetime import datetime

from django.urls import resolve, reverse_lazy

from rest_framework import status


def test_registry_API_endpoint_and_namespace_definition(client):
    """
    Test if there is a registry API endpoint and if is defined as "calls"
    namespace and "registry-list" as his name
    """

    url = '/api/v1/registry/'
    resolved = resolve(url)

    assert resolved.namespace == 'calls'\
        and resolved.url_name == 'registry-list'


def test_registry_API_endpoint_return_200_OK(client):
    """
    Test if Registry API Endpoint returns 200 Ok HTTP Status.
    """

    url = reverse_lazy('calls:registry-list')

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_POST_a_call_and_expect_job_id_and_data_posted(client):
    """
    Test POST a start call registry and expect a response from API containing
    a job_id and the data posted.
    """

    url = reverse_lazy('calls:registry-list')

    timestamp = datetime(2019, 4, 26, 20, 32, 10)

    start_call = {
            'type': 'start',
            'timestamp': timestamp.isoformat(),
            'call_id': 1,
            'source': '11111111111',
            'destination': '22222222222',
    }

    response = client.post(url, start_call, content_type='application/json')
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert 'job_id' in response_data

    for item in start_call.items():
        assert item in response_data['data'].items()
