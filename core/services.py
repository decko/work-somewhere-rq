from abc import ABC, abstractmethod


class ServiceAbstractClass(ABC):
    """
    This Abstract Service Class defines a template to process messages
    on Telephone application.

    message : dict
        The message to be processed.
    """

    trigger = None
    queue = None
    validation_class = None

    def __init__(self, *args, **kwargs):
        self.message = kwargs.get('message', None)

        if not self.trigger or not isinstance(self.trigger, str):
            raise Exception("A trigger must be a string and it is needed to accept any task.")

        if not self.queue or not isinstance(self.queue, str):
            raise Exception("A queue must be a string and it is needed to propagate the results.")

    @abstractmethod
    def obtainMessage(self):
        """
        Obtains the data needed to be processed.

        self.message could contain any information used to obtain the data
        or could be the date itself.
        """
        pass

    @abstractmethod
    def validateMessage(self):
        """
        Validates the message received.

        Validate the message received using validation class from
        validation_class attribute.
        """
        pass

    @abstractmethod
    def transformMessage(self):
        """
        Transform the validated message into something else needed.

        Transform the message to a new format used by other methods.
        """
        pass

    @abstractmethod
    def persistData(self):
        """
        Persist the data into a storage.

        Persist the data into a storage like a Django Model or something else.
        """
        pass

    @abstractmethod
    def propagateResult(self):
        """
        Propagate the result into a defined queue.

        Propagate the result into a defined queue to be processed by other
        Services.
        """
        pass

    def process(self):
        """
        Run all the methods to process a message and propagate the result.
        """

        self.obtainMessage()
        self.validateMessage()
        self.transformMessage()
        self.persistData()
        self.propagateResult()
