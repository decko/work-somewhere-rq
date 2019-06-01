import json
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

from core.services import ServiceAbstractClass

from .models import Bill


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
            'source_call_url': message.get('url'),
            'subscriber': message.get('source'),
            'destination': message.get('destination'),
            'start_timestamp': start_timestamp,
            'stop_timestamp': stop_timestamp,
            'call_duration': stop_timestamp - start_timestamp
        }

        day = timedelta(days=1)

        special_day_time = start_timestamp.replace(hour=6, minute=1, second=0)
        special_night_time = start_timestamp.replace(hour=22, minute=0, second=0)

        delta_seconds = timedelta()

        stop = stop_timestamp

        while(stop > special_day_time):
            if start_timestamp < special_day_time:
                start_timestamp = special_day_time

            if start_timestamp > special_night_time\
               and stop_timestamp < special_day_time + day:
                # condition for calls happened entirely between special time
                delta_seconds = timedelta(seconds=0)
                break

            if stop_timestamp > special_night_time:
                stop_timestamp = special_night_time

            delta_seconds = delta_seconds + (stop_timestamp - start_timestamp)

            special_day_time = special_day_time + day
            special_night_time = special_night_time + day

        minutes_call_duration = delta_seconds.seconds // 60

        bill['call_price'] = standing_charge + (minutes_call_duration * call_charge)

        self.data = bill
        return self.data

    def persistData(self):
        """
        Persist data to a storage.

        Expects a dict on self.data and persist it to a Bill model instance.

        :returns: Bill
            Returns a Bill instance.
        """

        assert self.data is not None and isinstance(self.data, dict), (
            'Make sure self.data is setted and it is a instance of dict.'
        )

        bill_data = self.data

        bill = Bill.objects.create(**bill_data)

        self.persisted_data = bill

    def propagateResult(self):
        pass

    def finishTask(self):
        super().finishTask()
