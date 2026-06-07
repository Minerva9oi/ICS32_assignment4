# NAME Bozhang Zhou 
# EMAIL bozhangz@uci.edu
# STUDENT ID 93213406


import json
import ds_protocol


def test_direct_message_msg():
    result = ds_protocol.direct_message_msg("abc123", "hello", "mark")
    data = json.loads(result)

    assert data["token"] == "abc123"
    assert data["directmessage"]["entry"] == "hello"
    assert data["directmessage"]["recipient"] == "mark"


def test_direct_message_new_msg():
    result = ds_protocol.direct_message_new_msg("abc123")
    data = json.loads(result)

    assert data["token"] == "abc123"
    assert data["directmessage"] == "new"


def test_direct_message_all_msg():
    result = ds_protocol.direct_message_all_msg("abc123")
    data = json.loads(result)

    assert data["token"] == "abc123"
    assert data["directmessage"] == "all"


def test_extract_json_message_response():
    json_msg = '{"response":{"type":"ok","message":"Direct message sent"}}'
    result = ds_protocol.extract_json(json_msg)

    assert result.type == "ok"
    assert result.message == "Direct message sent"
    assert result.token == ""
    assert result.messages == []


def test_extract_json_messages_response():
    json_msg = '{"response":{"type":"ok","messages":[{"message":"hi","from":"bob","timestamp":"1"}]}}'
    result = ds_protocol.extract_json(json_msg)

    assert result.type == "ok"
    assert result.message == ""
    assert len(result.messages) == 1
    assert result.messages[0]["message"] == "hi"
    assert result.messages[0]["from"] == "bob"