from abc import ABC


class ServiceAbstractClass(ABC):
    """
    This Abstract Service Class defines a template to process messages
    on Telephone application.
    """

    trigger = None
    queue = None
    message = None

    pass
