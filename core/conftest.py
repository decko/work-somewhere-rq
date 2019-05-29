import pytest

from .services import ServiceAbstractClass


@pytest.fixture(scope='function')
def sac_abstract_methods_mocker(mocker):
    """
    Fixture to mock the abstract methods of ServiceAbstractClass making
    it testable without asking for implementing all abstract methods on
    an instance.
    """

    mocker.patch.multiple(ServiceAbstractClass, __abstractmethods__=set())

    yield

    mocker.resetall()
