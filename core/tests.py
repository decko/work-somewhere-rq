from django.urls import resolve


def test_task_API_endpoint_and_namespace_definition(client):
    """
    Test if there is a Task API endpoint and if is defined as "core"
    namespace and "task-list" as his name
    """

    url = '/api/v1/task/'
    resolved = resolve(url)

    assert resolved.namespace == 'core'\
        and resolved.url_name == 'task-list'
