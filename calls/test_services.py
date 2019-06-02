import json
import pytest

from uuid import uuid4

from core.services import ServiceAbstractClass

from .models import Call
from .models import Registry
from .services import CallService
from .services import RegistryService

pytestmark = pytest.mark.django_db


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


def test_assertion_about_validation_class_attribute_on_RegistryService(mocker,
                                                                       start_call_fx):
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

    instance.startTask()
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
        def propagateResult(self):
            pass

    mocker.patch.multiple(TestService,
                          __abstractmethods__=set(),
                          trigger='call-service-done',
                          queue='test')

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

    del(TestService)


def test_for_failed_task_on_RegistryService_validateMessage(start_call_fx):
    """
    Test for when validateMessage get a non valid message, finishTask must
    set status to 'FAILED' and result must contains the error message.
    """

    start_call_fx['source'] = '0000000000'

    instance = RegistryService(message=start_call_fx)
    instance.job_id = uuid4()

    instance.startTask()
    instance.validateMessage()

    instance.task.refresh_from_db()
    assert instance.task.status == 'FAILED'
    assert 'The number is not a valid phone number'\
        in str(instance.result.get('source'))


def test_for_result_property_on_CallService_finishTask(start_call_fx, stop_call_fx):
    """
    Test for the result property on finishTask method, and his contents
    on the Task instance.
    """

    start_message = json.dumps(start_call_fx)

    instance = CallService(message=start_message)
    
    instance.job_id = uuid4()
    instance.startTask()
    instance.transformMessage()
    instance.persistData()
    instance.propagateResult()

    assert instance.result

    instance.finishTask()
    instance.task.refresh_from_db()

    assert instance.task.result == instance.result

    stop_message = json.dumps(stop_call_fx)

    instance = CallService(message=stop_message)

    instance.job_id = uuid4()
    instance.startTask()
    instance.transformMessage()
    instance.persistData()
    instance.propagateResult()

    assert instance.result

    instance.finishTask()
    instance.task.refresh_from_db()

    assert instance.task.result == instance.result
