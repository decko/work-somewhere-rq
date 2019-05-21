from core.services import ServiceAbstractClass


class RegistryService(ServiceAbstractClass):
    """
    RegistryService is a service responsible for new registries processing.
    """

    trigger = 'registry-service'
    queue = 'registry-service-done'
