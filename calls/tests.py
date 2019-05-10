import pytest
from datetime import datetime

from django.urls import resolve, reverse_lazy

from rest_framework import status


pytestmark = pytest.mark.django_db


@pytest.fixture
def start_call_fx():
    timestamp = datetime(2019, 4, 26, 12, 32, 10)
    call = {
            'type': 'start',
            'timestamp': timestamp.isoformat(),
            'call_id': 1,
            'source': '11111111111',
            'destination': '22222222222',
    }

    return call


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


def test_POST_a_call_and_expect_job_id_and_data_posted(client, start_call_fx):
    """
    Test POST a start call registry and expect a response from API containing
    a job_id and the data posted.
    """

    url = reverse_lazy('calls:registry-list')

    response = client.post(url, start_call_fx, content_type='application/json')
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert 'job_id' in response_data

    for item in start_call_fx.items():
        assert item in response_data['data'].items()


def test_expect_200Ok_response_GETting_a_job_id_URL(client, start_call_fx):
    """
    Test the job_id URL of a start call registry POST.
    """

    url = reverse_lazy('calls:registry-list')

    response = client.post(url, start_call_fx, content_type='application/json')
    response_data = response.json()

    task_url = response_data.get('job_id', None)

    task_response = client.get(task_url)

    assert task_response.status_code == status.HTTP_200_OK


def test_expect_status_property_about_registry_process(client, start_call_fx):
    """
    Test if there is a 'status' property in a response about registry process,
    and if it contains a 'DONE' status about this task.
    """

    url = reverse_lazy('calls:registry-list')

    response = client.post(url, start_call_fx, content_type='application/json')

    job_id = response.data.get('job_id')

    job = client.get(job_id)

    assert job.data.get('status') == 'DONE'


def test_expect_data_posted_return_encapsulated_on_message_property_on_response(client, start_call_fx):
    """
    Test if there is a 'result' property containing the result of registry
    process
    """

    url = reverse_lazy('calls:registry-list')

    response = client.post(url, start_call_fx, content_type='application/json')

    job_id = response.data.get('job_id')

    job = client.get(job_id)

    assert job.data.get('result')

    assert client.get(job.data.get('result')).status_code == status.HTTP_200_OK



def test_post_a_start_call_and_recover_it_using_a_GET_request(client, start_call_fx):
    """
    Test POST a start call registry to registry API and expect recover it
    using a GET request.
    """

    url = reverse_lazy('calls:registry-list')

    post_request = client.post(url,
                               start_call_fx,
                               content_type='application/json')

    assert post_request.status_code == status.HTTP_201_CREATED

    job_url = post_request.data.get('job_id')

    job_request = client.get(job_url)

    get_request = client.get(job_request.data.get('result'))

    response = get_request.json()

    assert get_request.status_code == status.HTTP_200_OK
    for key, value in start_call_fx.items():
        assert value == response.get(key)
