from core.services import ServiceAbstractClass

from .serializers import RegistrySerializer

class RegistryService(ServiceAbstractClass):
    """
    RegistryService is a service responsible for new registries processing.
    """

    trigger = 'registry-service'
    queue = 'registry-service-done'
    validation_class = RegistrySerializer

    def startTask(self):
        super().startTask()

    def obtainMessage(self):
        pass

    def validateMessage(self):
        """
        Uses RegistrySerializer to validate information obtained at
        self.message or on other variable.

        :returns: bool
            Returns True if message is valid and populates self.result

        self.registry: RegistrySerializer
            Is an instance of RegistrySerializer with the data if the message
            is valid.

        self.result: dict
            Contains the result of validation if the message is invalid.
        """
        assert self.validation_class is not None, (f'{self.__class__.__name__}'
                                                   ' must include a validation'
                                                   '_attribute or override '
                                                   'validateMessage method.')
    def transformMessage(self):
        pass

    def persistData(self):
        pass

    def propagateResult(self):
        pass

    def finishTask(self):
        super().finishTask()
