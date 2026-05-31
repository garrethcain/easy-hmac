from base64 import b64decode, b64encode
from datetime import datetime, timedelta, timezone
import hashlib
import hmac

from easy_hmac.exceptions import AuthenticationFailed
from easy_hmac.utils import http


def generate_hmac_sha256(
    secret: str, method: str, body: str, path: str, timestamp: str
) -> bytes:
    """Generate a SHA256 HMAC from HTTP request components.

    Args:
        secret: the key to use for the HMAC
        method: the http method. Likely POST.
        body: the data to generate the digest from
        path: the remote path. /remote/webhook/path
        timestamp: datetimestamp, GMT formatted as "%a, %d %b %Y %H:%M:%S GMT"

    Returns:
        bytes: the HMAC digest.
    """

    content_type: str = "application/json"
    _hash = hashlib.md5(body.encode(), usedforsecurity=False)
    content_md5 = b64encode(_hash.digest()).decode("utf-8")
    message_parts = [method, content_md5, content_type, timestamp, path]
    message = "\n".join(message_parts)
    signature = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), digestmod=hashlib.sha256
    )
    return signature.digest()


def _verify_hmac(secret: str, hmac_bytes: bytes, message_string: str) -> bool:
    """Verify an HMAC against an expected value using constant-time comparison.

    Args:
        secret: the key to use for the HMAC
        hmac_bytes: the hmac to be verified
        message_string: the message to use for the HMAC

    Returns:
        bool: True if the HMACs are equal, False otherwise
    """

    message_bytes: bytes = message_string.encode("utf-8")
    secret_bytes: bytes = secret.encode("utf-8")
    correct_hmac_bytes: bytes = hmac.new(
        secret_bytes, msg=message_bytes, digestmod=hashlib.sha256
    ).digest()
    return hmac.compare_digest(hmac_bytes, correct_hmac_bytes)


def verify_hmac(
    secret: str,
    hmac_base64: str,
    md5_body: str,
    raw_body: bytes,
    timestamp: str,
    content_type: str,
    path: str,
    request_method: str,
) -> bool:
    """Verify an incoming HMAC signature against the request components.

    Checks body integrity via MD5 hash and rejects requests older than
    15 minutes to prevent replay attacks.

    Args:
        secret: the shared secret key
        hmac_base64: base64-encoded HMAC from the Authorization header
        md5_body: base64-encoded MD5 hash from the Content-MD5 header
        raw_body: the raw request body as bytes
        timestamp: the Date header value
        content_type: the Content-Type header value
        path: the request path
        request_method: the HTTP method

    Returns:
        bool: True if verification succeeds

    Raises:
        AuthenticationFailed: if the signature is invalid, body was
            tampered, timestamp is malformed, or request is too old
    """

    try:
        request_time = datetime.fromtimestamp(
            http.parse_http_date(timestamp), timezone.utc
        )
    except ValueError as e:
        raise AuthenticationFailed("Malformed Date header") from e

    if abs(request_time - datetime.now(timezone.utc)) > timedelta(minutes=15):
        raise AuthenticationFailed("Request time too old")

    body_hash_b64 = b64encode(
        hashlib.new("md5", raw_body, usedforsecurity=False).digest()
    ).decode("utf-8")

    if body_hash_b64 != md5_body:
        raise AuthenticationFailed("HMAC Authentication Failed")

    hmac_bytes = b64decode(hmac_base64)

    message_parts = [
        request_method,
        body_hash_b64,
        content_type,
        timestamp,
        path,
    ]

    message = "\n".join(message_parts)

    if _verify_hmac(secret, hmac_bytes, message):
        return True

    raise AuthenticationFailed("HMAC Authentication Failed")
