import pytest

from abc import ABC

from calls.tests import start_call_fx

from .services import ServiceAbstractClass


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

    assert str(exception.value) == ('A trigger must be a string and it is '
                                    'needed to accept any task.')

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

    assert str(exception.value) == ('A queue must be a string and it is '
                                    'needed to propagate the results.')

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
