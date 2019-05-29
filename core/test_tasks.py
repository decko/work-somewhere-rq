def test_for_existence_of_a_dispatch_method():
    """
    Test for the existence of a dispatch method witch will be used
    """

    from core.tasks import dispatch

    assert callable(dispatch)
