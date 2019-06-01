import json
import pytest
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

from model_mommy import mommy

from .models import Bill
from .services import BillService


@pytest.fixture(scope="session")
def bills(django_db_setup, django_db_blocker):
    source = '99988526423'
    destination = '9933468278'

    calls = (
        (69, datetime(2019, 4, 26, 21, 57, 13),
         datetime(2019, 4, 26, 22, 17, 13), Decimal('0.54')),
        (70, datetime(2016, 2, 29, 12, 0, 0),
         datetime(2016, 2, 29, 14, 0, 0), Decimal('11.16')),
        (71, datetime(2017, 12, 11, 15, 7, 13),
         datetime(2017, 12, 11, 15, 14, 56), Decimal('0.99')),
        (72, datetime(2017, 12, 12, 22, 47, 56),
         datetime(2017, 12, 12, 22, 50, 56), Decimal('0.36')),
        (73, datetime(2017, 12, 12, 21, 57, 13),
         datetime(2017, 12, 12, 22, 10, 56), Decimal('0.54')),
        (74, datetime(2017, 12, 12, 4, 57, 13),
         datetime(2017, 12, 12, 6, 10, 56), Decimal('1.17')),
        (75, datetime(2017, 12, 13, 21, 57, 13),
         datetime(2017, 12, 14, 22, 10, 56), Decimal('86.85')),
        (76, datetime(2017, 12, 12, 15, 7, 58),
         datetime(2017, 12, 12, 15, 12, 56), Decimal('0.72')),
        (77, datetime(2018, 2, 28, 21, 57, 13),
         datetime(2018, 3, 1, 22, 10, 56), Decimal('86.85')),
    )

    with django_db_blocker.unblock():
        for call in calls:
            mommy.make(Bill,
                       source_call_url=f"/api/v1/calls/{call[0]}",
                       subscriber=source,
                       destination=destination,
                       start_timestamp=call[1],
                       stop_timestamp=call[2],
                       call_duration=call[2]-call[1],
                       call_price=call[3])

    bills = Bill.objects.all()

    yield bills

    with django_db_blocker.unblock():
        for bill in bills:
            bill.delete()


@pytest.fixture(scope='session')
def call():
    """
    Fixture containing a dict with the result of a successful CallService
    processing.
    """

    today = datetime.today()

    start_timestamp = today.replace(
        year=today.year if today.month > 1 else today.year - 1,
        month=today.month - 1 if today.month > 1 else 12,
        day=1)

    delta_timestamp = timedelta(minutes=10)

    stop_timestamp = start_timestamp + delta_timestamp

    call = {'url': '/calls/1',
            'call_id': 1,
            'start_timestamp': start_timestamp.isoformat(),
            'stop_timestamp': stop_timestamp.isoformat(),
            'source': '11111111111',
            'destination': '22222222222'}

    return call


@pytest.fixture(scope='session')
def bill(call, django_db_setup, django_db_blocker):
    """
    Fixture that insert a Bill instance and delete it when test is done.
    """

    message = json.dumps(call)

    instance = BillService(message=message)
    instance.transformMessage()
    with django_db_blocker.unblock():
        instance.persistData()

    yield instance.persisted_data

    with django_db_blocker.unblock():
        instance.persisted_data.delete()
