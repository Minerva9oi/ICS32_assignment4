# NAME Bozhang Zhou 
# EMAIL bozhangz@uci.edu
# STUDENT ID 93213406


import ds_messenger


def test_direct_message_default_values():
    message = ds_messenger.DirectMessage()

    assert message.recipient is None
    assert message.message is None
    assert message.timestamp is None


def test_direct_messenger_default_values():
    messenger = ds_messenger.DirectMessenger()

    assert messenger.dsuserver is None
    assert messenger.username is None
    assert messenger.password is None
    assert messenger.token is None


def test_send_with_empty_message():
    messenger = ds_messenger.DirectMessenger(
        dsuserver="127.0.0.1",
        username="testuser",
        password="testpass"
    )

    result = messenger.send("", "bob")

    assert result is False


def test_send_with_empty_recipient():
    messenger = ds_messenger.DirectMessenger(
        dsuserver="127.0.0.1",
        username="testuser",
        password="testpass"
    )

    result = messenger.send("hello", "")

    assert result is False


def test_retrieve_new_without_server():
    messenger = ds_messenger.DirectMessenger(
        dsuserver="127.0.0.1",
        username="testuser",
        password="testpass"
    )

    result = messenger.retrieve_new()

    assert result == []


def test_retrieve_all_without_server():
    messenger = ds_messenger.DirectMessenger(
        dsuserver="127.0.0.1",
        username="testuser",
        password="testpass"
    )

    result = messenger.retrieve_all()

    assert result == []