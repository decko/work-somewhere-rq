import json
import pytest
from uuid import uuid4
from copy import copy
from datetime import datetime

from django.urls import resolve, reverse_lazy

from rest_framework import status

from core.services import ServiceAbstractClass

from .services import RegistryService
from .services import CallService
from .models import Call
from .models import Registry

pytestmark = pytest.mark.django_db


@pytest.fixture
def start_call_fx():
    """
    Fixture that return a dict with a start call registry
    """

    timestamp = datetime(2019, 4, 26, 12, 32, 10)
    call = {
        'type': 'start',
        'timestamp': timestamp.isoformat(),
        'call_id': 1,
        'source': '11111111111',
        'destination': '22222222222',
    }

    return call


@pytest.fixture
def stop_call_fx():
    """
    Fixture that return a dict with a stop call registry
    """

    timestamp = datetime(2019, 4, 26, 12, 40, 10)
    call = {
        'type': 'stop',
        'timestamp': timestamp.isoformat(),
        'call_id': 1,
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

    Test uses start_call_fx fixture
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

    Test uses start_call_fx fixture
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

    Test uses start_call_fx fixture
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

    Test uses start_call_fx fixture
    """

    url = reverse_lazy('calls:registry-list')

    response = client.post(url, start_call_fx, content_type='application/json')

    job_id = response.data.get('job_id')

    job = client.get(job_id)

    result = job.json()

    assert result.get('result')

    registry_url = json.loads(result.get('result'))

    assert client.get(registry_url.get('url')).status_code == status.HTTP_200_OK



def test_post_a_start_call_and_recover_it_using_a_GET_request(client, start_call_fx):
    """
    Test POST a start call registry to registry API and expect recover it
    using a GET request.

    Test uses start_call_fx fixture
    """

    url = reverse_lazy('calls:registry-list')

    post_request = client.post(url,
                               start_call_fx,
                               content_type='application/json')

    assert post_request.status_code == status.HTTP_201_CREATED

    job_url = post_request.data.get('job_id')

    job_request = client.get(job_url)

    result = json.loads(job_request.data.get('result'))

    get_request = client.get(result.get('url'))

    response = get_request.json()

    assert get_request.status_code == status.HTTP_200_OK
    for key, value in start_call_fx.items():
        assert value == response.get(key)


def test_GET_call_api_and_return_200Ok(client):
    """
    Test a GET request on the Call API Endpoint and expect it return 200 Ok
    """

    url = '/api/v1/calls/'

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_namespace_of_call_api_endpoint():
    """
    Test if there is a Call API endpoint and if is defined as "calls"
    namespace and "call-list" as his name
    """

    url = '/api/v1/calls/'
    resolved = resolve(url)

    assert resolved.namespace == 'calls'\
        and resolved.url_name == 'call-list'


def test_documentation_for_call_view():
    """
    Test for documentation on Call API Endpoint view
    """

    url = reverse_lazy('calls:call-list')
    view = resolve(url).func

    assert view.__doc__


def test_post_a_start_and_stop_registry_and_get_a_call(client, start_call_fx,
                                                       stop_call_fx):
    """
    Test POSTing a start and a stop registry and expect get it
    at Call API Endpoint

    Test uses start_call_fx fixture
    Test uses stop_call_fx fixture
    """

    post_url = reverse_lazy('calls:registry-list')

    post_data = [start_call_fx, stop_call_fx]

    for data in post_data:
        response = client.post(post_url, data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    get_url = reverse_lazy('calls:call-list')

    response = client.get(get_url)

    assert len(response.data) == 1
    assert response.data[0].get('start_timestamp')
    assert response.data[0].get('stop_timestamp')


def test_post_a_start_and_stop_registry_and_get_a_call_using_url(client,
                                                                 start_call_fx,
                                                                 stop_call_fx):
    """
    Test POSTing a start and a stop registry and expect get it
    at Call API Endpoint using a call_id

    Test uses start_call_fx fixture
    Test uses stop_call_fx fixture
    """

    post_url = reverse_lazy('calls:registry-list')

    post_data = [start_call_fx, stop_call_fx]

    for data in post_data:
        response = client.post(post_url, data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    get_url = reverse_lazy('calls:call-detail', kwargs={'call_id': 1})

    response = client.get(get_url)

    assert response.data.get('start_timestamp')
    assert response.data.get('stop_timestamp')


def test_post_a_start_registry_with_invalid_phone_number(client, start_call_fx):
    """
    Test POSTing a start registry with invalid phone number and expect
    something

    Test uses start_call_fx fixture
    """

    from calls.serializers import RegistrySerializer

    start_call_fx['source'] = '01111111111'

    registry = RegistrySerializer(data=start_call_fx)

    assert not registry.is_valid()


def test_call_api_return_only_consolidated_calls(client, start_call_fx, stop_call_fx):
    """
    Test POSTing two start registries and only one stop registry and expect
    to GET only on record on Call API Endpoint.

    Test uses start_call_fx fixture
    Test uses stop_call_fx fixture
    """

    post_url = reverse_lazy('calls:registry-list')

    start_call_fx_2 = copy(start_call_fx)
    start_call_fx_2['call_id'] = 2

    post_data = [start_call_fx, start_call_fx_2, stop_call_fx]

    for data in post_data:
        response = client.post(post_url, data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    get_url = reverse_lazy('calls:call-list')

    response = client.get(get_url)

    assert len(response.data) == 1


def test_for_a_registry_service_abstract_class():
    """
    Test for a RegistryService existence.
    """

    assert RegistryService


def test_for_RegistryService_as_a_ServiceAbstractClass_subclass():
    """
    Test for RegistryService as a ServiceAbstractClass subclass.
    """

    assert issubclass(RegistryService, ServiceAbstractClass)


def test_for_RegistryService_documentation():
    """
    Test for RegistryService documentation on class docstring.
    """

    assert RegistryService.__doc__


def test_for_RegistryService_trigger_and_queue_attributes():
    """
    Test for the values of trigger and queue attribute.
    """

    assert RegistryService.trigger == 'registry-service'
    assert RegistryService.queue == 'registry-service-done'


def test_for_RegistryService_instance():
    """
    Test for a RegistryService instance.
    """

    instance = RegistryService()

    assert isinstance(instance, RegistryService)


def test_for_RegistryService_startTask_method():
    """
    Test for RegistryService startTask method.
    Expect to find a new Task instance with 'status' value as 'STARTED'.
    """

    message = {'a': 'b'}

    instance = RegistryService(message=message, job_id=uuid4())
    instance.startTask()

    instance.task.refresh_from_db()

    assert instance.task
    assert instance.task.status == 'STARTED'


def test_for_RegistryService_finishTask_method():
    """
    Test for RegistryService finishTask method.
    Expect to find a Task instance with 'status' value as 'DONE'.
    """

    message = {'a': 'b'}

    instance = RegistryService(message=message, job_id=uuid4())
    instance.startTask()
    instance.finishTask()

    instance.task.refresh_from_db()

    assert instance.task
    assert instance.task.status == 'DONE'


def test_assertion_about_validation_class_attribute_on_RegistryService(mocker):
    """
    Test for assertion about validation_class attribute on RegistryService
    validateMessage method.
    """

    mocker.patch.object(RegistryService, 'validation_class', None)
    instance = RegistryService(message=start_call_fx, job_id=uuid4())

    with pytest.raises(AssertionError) as exception:
        instance.validateMessage()

    mocker.resetall()

    assert str(exception.value) == ('RegistryService must include a validation_'
                                    'attribute or override validateMessage '
                                    'method.')


def test_for_RegistryService_validateMessage_method_return(start_call_fx):
    """
    Test for RegistryService validateMessage method return given a valid
    message.

    Expect method to return True.

    Test uses start_call_fx fixture.
    """

    instance = RegistryService(message=start_call_fx, job_id=uuid4())
    instance.validateMessage()

    assert instance.is_valid is True


def test_for_RegistryService_persistData_to_return_a_Registry_instance(start_call_fx):
    """
    Test for RegistryService persistData method return a Registry instance.

    Test uses start_call_fx fixture.
    """

    instance = RegistryService(message=start_call_fx, job_id=uuid4())
    instance.validateMessage()

    registry = instance.persistData()

    assert registry
    assert isinstance(registry, Registry)


def test_for_RegistryService_persistData_raise_AssertionError_if_not_is_valid():
    """
    Test for RegistryService persistData method to raise a AssertionError if
    is_valid is not set or if it is False.
    """

    instance = RegistryService(message={'a', 'b'}, job_id=uuid4())
    instance.validateMessage()

    with pytest.raises(AssertionError) as exception:
        instance.persistData()

    assert str(exception.value) == ('You must override the persistData method'
                                    ' if you want to persist the data without'
                                    ' validating it first.')


def test_for_a_CallService_class():
    """
    Test for a CallService existence.
    """

    assert CallService


def test_for_CallService_as_a_ServiceAbstractClass_subclass():
    """
    Test for CallService as a ServiceAbstractClass subclass.
    """

    assert issubclass(CallService, ServiceAbstractClass)


def test_for_a_CallService_documentation():
    """
    Test for RegistryService documentation on class docstring.
    """

    assert CallService.__doc__


def test_for_CallService_trigger_and_queue_attributes():
    """
    Test for the values of trigger and queue attribute.
    """

    assert CallService.trigger == 'registry-service-done'
    assert CallService.queue == 'call-service-done'


def test_for_CallService_instance():
    """
    Test for a CallService instance.
    """

    instance = CallService()

    assert isinstance(instance, CallService)


def test_for_CallService_transformMessage_method(start_call_fx):
    """
    Test for CallService transformMessage method to translate a
    message com RegistryService to a dict witch will be consumed
    by Call model.

    Test uses start_call_fx fixture.
    """

    message = json.dumps(start_call_fx)

    instance = CallService(message=message)
    call_data = instance.transformMessage()

    keys = {'start_timestamp', 'source', 'destination', 'call_id'}

    assert keys == call_data.keys()

    del(start_call_fx['type'])
    for value in start_call_fx.values():
        assert value in call_data.values()


def test_for_CallService_persistData_method(start_call_fx):
    """
    Test for CallService persistData method to create or update a
    Call model instance given a translated message.
    Expect it to return a Call instance.

    Test uses start_call_fx fixture.
    """

    message = json.dumps(start_call_fx)

    instance = CallService(message=message)
    instance.transformMessage()

    call = instance.persistData()

    assert isinstance(call, Call)
    assert call.start_timestamp == start_call_fx.get('timestamp')


def test_for_CallService_propagateResult_method(start_call_fx, stop_call_fx,
                                                mocker):
    """
    Test for CallService propagateResult method. Given a consolidated
    call instance, propagate a serialized message to queue attribute.

    Test uses start_call_fx fixture.
    Test uses stop_call_fx fixture.
    Test uses mocker.
    """

    class TestService(ServiceAbstractClass):
        """
        Just a TestService to mock a ServiceClass
        """
        trigger = 'call-service-done'
        queue = 'test'

        def propagateResult(self):
            pass

    mocker.patch.multiple(TestService, __abstractmethods__=set())

    start_message = json.dumps(start_call_fx)

    start_instance = CallService(message=start_message)
    start_instance.transformMessage()
    start_instance.persistData()

    start_call = start_instance.propagateResult()

    assert not start_call

    stop_message = json.dumps(stop_call_fx)

    stop_instance = CallService(message=stop_message)
    stop_instance.transformMessage()
    stop_instance.persistData()

    stop_call = stop_instance.propagateResult()

    assert stop_call

    mocker.resetall()
