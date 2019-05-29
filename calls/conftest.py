import pytest

from datetime import datetime


@pytest.fixture
def start_call_fx():
    """
    Fixture that return a dict with a start call registry
    """

    timestamp = datetime(2019, 4, 26, 12, 32, 10)
    call = {
        'type': 'start',
        'timestamp': timestamp.isoformat(),
        'call_id': 1,
        'source': '11111111111',
        'destination': '22222222222',
    }

    return call


@pytest.fixture
def stop_call_fx():
    """
    Fixture that return a dict with a stop call registry
    """

    timestamp = datetime(2019, 4, 26, 12, 40, 10)
    call = {
        'type': 'stop',
        'timestamp': timestamp.isoformat(),
        'call_id': 1,
    }

    return call
