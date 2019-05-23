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
    call_charge = Decimal('0.09')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.standing_charge is not None\
                and isinstance(self.standing_charge, Decimal),\
                ('A standing_charge value must be a Decimal type and set '
                 'to make this service work as expected.')

        assert self.call_charge is not None\
                and isinstance(self.call_charge, Decimal), \
                ('A call_charge value must be a Decimal type and set '
                 'to make this service work as expected.')

    def startTask(self):
        super().startTask()

    def obtainMessage(self):
        pass

    def validateMessage(self):
        pass

    def transformMessage(self):
        message = json.loads(self.message)
        standing_charge = self.standing_charge
        call_charge = self.call_charge

        start_timestamp = datetime.fromisoformat(message.get('start_timestamp'))
        stop_timestamp = datetime.fromisoformat(message.get('stop_timestamp'))

        bill = {
            'subscriber': message.get('source'),
            'destination': message.get('destination'),
            'start_timestamp': start_timestamp,
            'stop_timestamp': stop_timestamp,
            'call_duration': stop_timestamp - start_timestamp
        }

        special_night_time = stop_timestamp.replace(hour=22, minute=0,
                                                    second=0)

        if stop_timestamp > special_night_time:
            stop_timestamp = special_night_time

        minutes_call_duration = (stop_timestamp - start_timestamp).seconds // 60

        bill['call_price'] = standing_charge + (minutes_call_duration * call_charge)

        self.data = bill
        return self.data

    def persistData(self):
        pass

    def propagateResult(self):
        pass

    def finishTask(self):
        super().finishTask()
