import json
from datetime import datetime
from decimal import Decimal

from core.services import ServiceAbstractClass


class BillService(ServiceAbstractClass):
    """
    BillService is a service responsible for billing consolidated calls.
    """

    trigger = 'call-service-done'
    queue = 'bill-service-done'
    standing_charge = Decimal('0.36')

    def __init__(self):
        assert self.standing_charge is not None\
                and isinstance(self.standing_charge, Decimal), \
                ('A standing_charge value must be a Decimal type and set '
                 'to make this service work as expected.')

        super().__init__()

    def startTask(self):
        super().startTask()

    def obtainMessage(self):
        pass

    def validateMessage(self):
        pass

    def transformMessage(self):
        message = json.loads(self.message)

        bill = {
            'subscriber': message.get('source'),
            'destination': message.get('destination'),
            'start_timestamp': datetime.fromisoformat(message.get('start_timestamp')),
            'stop_timestamp': datetime.fromisoformat(message.get('stop_timestamp')),
        }
        bill['call_duration'] = bill['stop_timestamp'] - bill['start_timestamp']
        bill['call_price'] = Decimal(0.30)

        self.data = bill
        return self.data

    def persistData(self):
        pass

    def propagateResult(self):
        pass

    def finishTask(self):
        super().finishTask()
