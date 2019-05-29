import pytest

from abc import ABC
from uuid import uuid4

from django.urls import resolve, reverse

from rest_framework import status

from .services import ServiceAbstractClass


pytestmark = pytest.mark.django_db


def test_if_theres_a_schema_url_for_metadata_and_documentation(client):
    """
    Test if there is a schema URL for metadata and documentation.
    """

    url = reverse('docs')

    response = client.get(url)

    assert url
    assert response.status_code == status.HTTP_200_OK


def test_task_API_endpoint_and_namespace_definition(client):
    """
    Test if there is a Task API endpoint and if is defined as "core"
    namespace and "task-list" as his name
    """

    url = '/api/v1/task/'
    resolved = resolve(url)

    assert resolved.namespace == 'core'\
        and resolved.url_name == 'task-list'


def test_documentation_for_task_view():
    """
    Test if there is documentation for the Task API Endpoint
    """

    url = reverse('core:task-list')
    view = resolve(url).func

    assert view.__doc__


def test_return_404_when_a_Task_is_not_found(client):
    """
    Test if a 404 Http status is returned when a Task is not found.
    """

    url = reverse('core:task-detail', kwargs={'job_id': uuid4()})

    request = client.get(url)

    assert request.status_code == status.HTTP_404_NOT_FOUND
