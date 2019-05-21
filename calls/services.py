from core.services import ServiceAbstractClass


class RegistryService(ServiceAbstractClass):
    """
    RegistryService is a service responsible for new registries processing.
    """

    trigger = 'registry-service'
    queue = 'registry-service-done'

    def startTask(self):
        pass

    def obtainMessage(self):
        pass

    def validateMessage(self):
        pass

    def transformMessage(self):
        pass

    def persistData(self):
        pass

    def propagateResult(self):
        pass

    def finishTask(self):
        pass
