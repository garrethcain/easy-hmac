import datetime
import hashlib
import hmac as hmac_mod
from base64 import b64encode

import pytest

from easy_hmac import core, exceptions


@pytest.fixture
def token():
    return {
        "name": "test-token",
        "secret": "6ff2dc141c0841e2a43c25be9ae9b097",
        "identifier": "2e42a19593f047e080285e49864b0fb6",
    }


def _compute_dummy_request(token, body, timestamp):
    method = "GET"
    path = "/api/v1/my/request"
    content_type = "application/json"

    body_hash = hashlib.md5(body.encode(), usedforsecurity=False)
    content_md5 = b64encode(body_hash.digest()).decode("utf-8")
    message_parts = [method, content_md5, content_type, timestamp, path]
    message = "\n".join(message_parts)

    signature = hmac_mod.new(
        token["secret"].encode("utf-8"),
        message.encode("utf-8"),
        digestmod=hashlib.sha256,
    )
    hmac_base64 = b64encode(signature.digest()).decode("utf-8")

    headers = {
        "Date": timestamp,
        "Content-MD5": content_md5,
        "Content-Type": content_type,
        "Authorization": "HMAC {}:{}".format(token["identifier"], hmac_base64),
    }

    return {"method": method, "body": body, "path": path, "headers": headers}


def _extract_hmac_from_request(request):
    auth_header = request["headers"]["Authorization"]
    _, auth_string = auth_header.split(" ")
    _, hmac_base64 = auth_string.split(":")
    return hmac_base64


def test_verify_hmac(token):
    timestamp = datetime.datetime.now(datetime.UTC).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    request = _compute_dummy_request(token, "", timestamp)

    actual = core.verify_hmac(
        token["secret"],
        _extract_hmac_from_request(request),
        request["headers"]["Content-MD5"],
        request["body"].encode(),
        request["headers"]["Date"],
        request["headers"]["Content-Type"],
        request["path"],
        request["method"],
    )

    assert actual is True


def test_verify_hmac_wrong_secret(token):
    timestamp = datetime.datetime.now(datetime.UTC).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    request = _compute_dummy_request(token, "", timestamp)

    with pytest.raises(exceptions.AuthenticationFailed):
        core.verify_hmac(
            "wrong-secret",
            _extract_hmac_from_request(request),
            request["headers"]["Content-MD5"],
            request["body"].encode(),
            request["headers"]["Date"],
            request["headers"]["Content-Type"],
            request["path"],
            request["method"],
        )


def test_verify_hmac_malformed_timestamp(token):
    malformed_timestamp = "Sunday Dec 31 23:59:37 1999"
    request = _compute_dummy_request(token, "", malformed_timestamp)

    with pytest.raises(exceptions.AuthenticationFailed):
        core.verify_hmac(
            token["secret"],
            _extract_hmac_from_request(request),
            request["headers"]["Content-MD5"],
            request["body"].encode(),
            request["headers"]["Date"],
            request["headers"]["Content-Type"],
            request["path"],
            request["method"],
        )


def test_verify_hmac_timestamp_too_old(token):
    old_timestamp = "Fri, 10 Dec 2021 00:16:57 GMT"
    request = _compute_dummy_request(token, "", old_timestamp)

    with pytest.raises(exceptions.AuthenticationFailed):
        core.verify_hmac(
            token["secret"],
            _extract_hmac_from_request(request),
            request["headers"]["Content-MD5"],
            request["body"].encode(),
            request["headers"]["Date"],
            request["headers"]["Content-Type"],
            request["path"],
            request["method"],
        )


def test_verify_hmac_wrong_body(token):
    timestamp = datetime.datetime.now(datetime.UTC).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    request = _compute_dummy_request(token, "", timestamp)

    with pytest.raises(exceptions.AuthenticationFailed):
        core.verify_hmac(
            token["secret"],
            _extract_hmac_from_request(request),
            request["headers"]["Content-MD5"],
            b"{'hello': 'world'}",
            request["headers"]["Date"],
            request["headers"]["Content-Type"],
            request["path"],
            request["method"],
        )


def test_generate_hmac():
    secret = "79721503-d1ef-46b7-b4ca-fec39ece902f"
    body = '{"event": "lifecycle_updated", "payload": {"uuid": "cb8c79cd-8d79-4698-90a2-662eeab8da98", "timestamp": "2021-12-10T00:16:08.048401Z", "status": "PROCESSING"}}'
    method = "POST"
    timestamp = "Fri, 10 Dec 2021 00:16:57 GMT"
    path = ""
    result_digest = core.generate_hmac_sha256(secret, method, body, path, timestamp)
    actual_signature = b64encode(result_digest).decode()
    expected_signature = "0dKZk1RdhvdMP6aDZyltwiWoAiEW3P32p0ihMts2K6o="
    assert actual_signature == expected_signature
