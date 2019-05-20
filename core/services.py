from abc import ABC


class ServiceAbstractClass(ABC):
    """
    This Abstract Service Class defines a template to process messages
    on Telephone application.
    """

    trigger = None
    queue = None
    message = None

    def __init__(self):

        if not self.trigger or not isinstance(self.trigger, str):
            raise Exception("A trigger must be a string and it is needed to accept any task.")
