import pytest

from abc import ABC
from uuid import uuid4

from django.urls import resolve, reverse

from rest_framework import status

from calls.tests import start_call_fx

from .services import ServiceAbstractClass


pytestmark = pytest.mark.django_db


@pytest.fixture(scope='function')
def sac_abstract_methods_mocker(mocker):
    """
    Fixture to mock the abstract methods of ServiceAbstractClass making
    it testable without asking for implementing all abstract methods on
    an instance.
    """

    mocker.patch.multiple(ServiceAbstractClass, __abstractmethods__=set())

    yield

    mocker.resetall()


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


def test_for_a_task_abstract_class():
    """
    Test for the existence of a ServiceAbstractClass to import.
    """

    assert ServiceAbstractClass


def test_for_serviceabstractclass_as_abstract_class_instance():
    """
    Test for ServiceAbstractClass is a abstract base class(ABC) instance
    """

    assert issubclass(ServiceAbstractClass, ABC)


def test_for_some_serviceabstractclass_attributes():
    """
    Test for a list of attributes that ServiceAbstractClass must implement.
    """

    attributes = {'trigger', 'queue', 'validation_class'}

    for attribute in attributes:
        assert hasattr(ServiceAbstractClass, attribute)


def test_for_initial_validation_when_instantiate_serviceabstractclass(sac_abstract_methods_mocker):
    """
    Test if a instance of ServiceAbstractClass raises an exception when
    instantiated without value for 'trigger' attribute.

    Test use sac_abstract_methods_mocker fixture.
    """

    class TestService(ServiceAbstractClass):
        pass

    with pytest.raises(Exception) as exception:
        TestService()

    assert str(exception.value) == 'A trigger must be a string and it is needed to accept any task.'

    del(TestService)


def test_for_queue_parameter_initial_validation_when_instantiate_serviceabstractclass(sac_abstract_methods_mocker):
    """
    Test if a instance of ServiceAbstractClass raises an exception when
    instantiated without value for 'queue' attribute.

    Test use sac_abstract_methods_mocker fixture.
    """

    class TestService(ServiceAbstractClass):
        trigger = 'test'
        pass

    with pytest.raises(Exception) as exception:
        TestService()

    assert str(exception.value) == 'A queue must be a string and it is needed to propagate the results.'

    del(TestService)


def test_for_serviceabstractclass_abstract_methods():
    """
    Test for abstract methods of ServiceAbstractClass. Expect to find the
    following list 'obtainMessage', 'validateMessage', 'transformMessage',
    'persistData', 'propagateResult', 'startTask', 'finishTask'.
    """

    methods = {'obtainMessage', 'validateMessage', 'transformMessage',
               'persistData', 'propagateResult', 'startTask', 'finishTask'}

    assert ServiceAbstractClass.__abstractmethods__ == methods


def test_for_process_method_on_serviceabstractclass():
    """
    Test for the process method used to run all methods at once.
    """

    assert ServiceAbstractClass.process


def test_for_existence_of_a_dispatch_method():
    """
    Test for the existence of a dispatch method witch will be used
    """

    from core.tasks import dispatch

    assert callable(dispatch)


def test_extract_subsclass_information_from_ServiceAbstractClass(sac_abstract_methods_mocker, mocker):
    """
    Test for extract the subclasses from ServiceAbstractClass.

    Test use sac_abstract_methods_mocker fixture.
    """

    class RegistryValidationService(ServiceAbstractClass):
        trigger = 'registry-validation'
        queue = 'registry-q'

    class RegistryPersistenceService(ServiceAbstractClass):
        trigger = 'registry-persistence'
        queue = 'registry-q'

    mocker.patch.object(ServiceAbstractClass, '__subclasses__')
    subclasses = [RegistryValidationService, RegistryPersistenceService]
    ServiceAbstractClass.__subclasses__.return_value = subclasses

    services = ServiceAbstractClass.__subclasses__()

    assert len(services) == 2

    mocker.resetall()

    del(RegistryValidationService)
    del(RegistryPersistenceService)


def test_build_a_dict_using_trigger_attribute_from_all_ServiceAbstractClass_subclasses(sac_abstract_methods_mocker, mocker):
    """
    Test for build a dict with the trigger attribute from all
    ServiceAbstractClass subclasses.

    Test use sac_abstract_methods_mocker fixture.
    """

    class RegistryValidationService(ServiceAbstractClass):
        trigger = 'registry-validation'
        queue = 'registry-q'

    class RegistryPersistenceService(ServiceAbstractClass):
        trigger = 'registry-persistence'
        queue = 'registry-q'

    subclasses = [RegistryValidationService, RegistryPersistenceService]
    mocker.patch.object(ServiceAbstractClass, '__subclasses__')
    ServiceAbstractClass.__subclasses__.return_value = subclasses

    services = ServiceAbstractClass.__subclasses__()

    triggers = {service.trigger: service for service in services}

    assert len(triggers) == 2
    assert 'registry-validation' in triggers.keys()
    assert 'registry-persistence' in triggers.keys()
    assert 'RegistryValidationService' in str(triggers.values())
    assert 'RegistryPersistenceService' in str(triggers.values())

    mocker.resetall()

    del(RegistryValidationService)
    del(RegistryPersistenceService)


def test_select_a_service_class_based_on_trigger_value(sac_abstract_methods_mocker):
    """
    Test for select a service class based on trigger value.

    Test use sac_abstract_methods_mocker fixture.
    """

    class RegistryValidationService(ServiceAbstractClass):
        trigger = 'registry-validation'
        queue = 'registry-q'

    class RegistryPersistenceService(ServiceAbstractClass):
        trigger = 'registry-persistence'
        queue = 'registry-q'

    trigger = 'registry-validation'

    services = ServiceAbstractClass.__subclasses__()

    triggers = {service.trigger: service for service in services}

    service = triggers.get(trigger)

    assert service == RegistryValidationService

    del(RegistryValidationService)
    del(RegistryPersistenceService)


def test_instanciate_a_service_class_using_trigger_and_message(sac_abstract_methods_mocker, start_call_fx):
    """
    Test for create a instance of a ServiceClass using trigger and
    message.

    Test use sac_abstract_methods_mocker fixture.
    """

    class RegistryValidationService(ServiceAbstractClass):
        trigger = 'registry-validation'
        queue = 'registry-q'

    class RegistryPersistenceService(ServiceAbstractClass):
        trigger = 'registry-persistence'
        queue = 'registry-q'

    trigger = 'registry-validation'

    services = ServiceAbstractClass.__subclasses__()

    triggers = {service.trigger: service for service in services}

    service = triggers.get(trigger)(start_call_fx)

    assert isinstance(service, RegistryValidationService)

    del(RegistryValidationService)
    del(RegistryPersistenceService)


def test_dispatch_a_message_without_any_ServiceAbstractClass_subclasses(start_call_fx, mocker):
    """
    Test for dispatching a message without any ServiceAbstractClass.
    Expect for a raised Exception.

    Test use start_call_fx fixture.
    """

    from core.tasks import dispatch

    mocker.patch.multiple(ServiceAbstractClass, __subclasses__=list)

    with pytest.raises(Exception) as exception:
        dispatch(start_call_fx, 'anything')

    assert str(exception.value) == ('No ServiceAbstractClass subclass has been'
                                    ' found. You need to create a new class '
                                    'inherit it to make dispatch works.')

    mocker.resetall()


def test_dispatch_a_message_without_matching_any_available_trigger(start_call_fx):
    """
    Test for dispatching a message with a trigger that don't match to
    any ServiceAbstractClass subclass available.

    Test use start_call_fx fixture.
    """

    class RegistryValidationService(ServiceAbstractClass):
        trigger = 'registry-validation'
        queue = 'registry-q'

    from core.tasks import dispatch

    with pytest.raises(Exception) as exception:
        dispatch(start_call_fx, 'anything')

    assert str(exception.value) == ('No trigger available to match your '
                                    'request. Verify if there is any '
                                    'ServiceAbstractClass subclass with '
                                    'this trigger.')

    del(RegistryValidationService)
