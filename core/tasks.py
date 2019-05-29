from django_rq import job

from .services import ServiceAbstractClass

from calls.services import CallService
from calls.services import RegistryService
from bills.services import BillService


@job
def dispatch(message, trigger, *args, **kwargs):
    """
    Receives a message and a trigger witch will be used to determine
    what to do with the message in witch queue.

    Parameters
    ----------
    message : dict
        The message containing data or a locator to get it.

    trigger : str
        A string containing a trigger to witch service to run
    """

    services = ServiceAbstractClass.__subclasses__()

    if not services:
        raise Exception('No ServiceAbstractClass subclass has been'
                        ' found. You need to create a new class '
                        'inherit it to make dispatch works.')

    triggers = {service.trigger: service for service in services}

    service_cls = triggers.get(trigger)

    if not service_cls:
        raise Exception('No trigger available to match your '
                        'request. Verify if there is any '
                        'ServiceAbstractClass subclass with '
                        'this trigger.')

    service = service_cls(message=message, *args, **kwargs)

    service.process()
