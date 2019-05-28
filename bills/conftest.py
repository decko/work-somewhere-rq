import json
import pytest
from datetime import datetime
from decimal import Decimal

from model_mommy import mommy

from .models import Bill
from .services import BillService


@pytest.fixture(scope="session")
def bills(django_db_setup, django_db_blocker):
    source = '99988526423'
    destination = '9933468278'

    calls = (
        (70, datetime(2019, 4, 26, 21, 57, 13), datetime(2019, 4, 26, 22, 17, 13), Decimal('0.54')),
        (71, datetime(2017, 12, 11, 15, 7, 13), datetime(2017, 12, 12, 22, 50, 56), Decimal('123.75')),
        (72, datetime(2017, 12, 12, 22, 47, 56), datetime(2017, 12, 12, 22, 50, 56), Decimal('125.64')),
        (73, datetime(2017, 12, 12, 21, 57, 13), datetime(2017, 12, 12, 22, 10, 56), Decimal('0.54')),
        (74, datetime(2017, 12, 12, 4, 57, 13), datetime(2017, 12, 12, 6, 10, 56), Decimal('1.17')),
        (75, datetime(2017, 12, 13, 21, 57, 13), datetime(2017, 12, 14, 22, 10, 56), Decimal('86.85')),
        (76, datetime(2017, 12, 12, 15, 7, 58), datetime(2017, 12, 12, 15, 12, 56), Decimal('0.72')),
        (77, datetime(2018, 2, 28, 21, 57, 13), datetime(2018, 3, 1, 22, 10, 56), Decimal('86.85')),
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


@pytest.fixture
def call():
    """
    Fixture containing a dict with the result of a successful CallService
    processing.
    """

    call = {'url': '/calls/1',
            'call_id': 1,
            'start_timestamp': '2019-04-26T12:32:10',
            'stop_timestamp': '2019-04-26T12:40:10',
            'source': '11111111111',
            'destination': '22222222222'}

    return call


@pytest.fixture
def bill(call):
    """
    Fixture that insert a Bill instance and delete it when test is done.
    """

    message = json.dumps(call)

    instance = BillService(message=message)
    instance.transformMessage()
    instance.persistData()

    yield instance.persisted_data

    instance.persisted_data.delete()

