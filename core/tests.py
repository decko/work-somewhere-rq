from django.urls import resolve, reverse

from rest_framework import status


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
