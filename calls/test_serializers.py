def test_post_a_start_registry_with_invalid_phone_number(client, start_call_fx):
    """
    Test POSTing a start registry with invalid phone number and expect
    something

    Test uses start_call_fx fixture
    """

    from calls.serializers import RegistrySerializer

    start_call_fx['source'] = '01111111111'

    registry = RegistrySerializer(data=start_call_fx)

    assert not registry.is_valid()
