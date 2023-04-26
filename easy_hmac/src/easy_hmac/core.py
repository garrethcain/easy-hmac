from base64 import b64decode, b64encode
from easy_hmac import exceptions
from easy_hmac.utils import http
from datetime import datetime, timezone, timedelta
import hashlib
import hmac


def generate_hmac_sha256(
    secret: str, method: str, body: str, path: str, timestamp: str
):
    """Generate a SHA256 HMAC from two strings

    Args:
        secret: the key to use for the HMAC
        method: the http method. Likely POST.
        body: the data to generate the digest from
        path: the remote path. /remote/webhook/path
        timestamp: datetimestamp, GMT formatted as "%a, %d %b %Y %H:%M:%S GMT"
    Returns:
        str: the HMAC digest.
    """

    contentType: str = "application/json"
    _hash = hashlib.md5(body.encode())
    contentMD5 = b64encode(_hash.digest()).decode("utf-8")
    message_parts = [method, contentMD5, contentType, timestamp, path]
    message = "\n".join(message_parts)
    signature = hmac.new(
        bytes(secret, "latin-1"), bytes(message, "latin-1"), digestmod=hashlib.sha256
    )
    return signature.digest()


def __verify_hmac(secret: str, hmac_bytes: bytes, message_string: str) -> bool:
    """
    Verifies if the hmac generated by message_string and secret is the same as hmac_bytes.
    This function is used by verify_hmac

    Args:
        secret: the key to use for the HMAC
        hmac_bytes: the hmac to be verified
        message_string: the message to use for the HMAC

    Returns:
        boolean: True if the HMACs are equal, False otherwise
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
):
    """
    Verifies if the hmac generated by the parameters and secret is the same as
    the one by hmac_base64.

    Args:
        secret: the key to use for the HMAC
        hmac_base64: a given hmac
        md5_body:
        raw_body:
        timestamp:
        content_type:
        path:
        request_method:

    Returns:
        boolean: True if the HMACs are equal, False otherwise
    """

    # check if timestamp is valid before verifying the HMAC
    try:
        request_time = datetime.fromtimestamp(
            http.parse_http_date(timestamp), timezone.utc
        )
    except ValueError as e:
        raise exceptions.AuthenticationFailed("Malformed Date header") from e

    if abs(request_time - datetime.now(timezone.utc)) > timedelta(minutes=15):
        raise exceptions.AuthenticationFailed("Request time too old")

    # define auth_failed here so we can raise the exception easily
    auth_failed = exceptions.AuthenticationFailed("HMAC Authentication Failed")

    # ensure that the base64 md5 hash computed from the ENCODED raw body is the 
    # same as the one present on md5_body
    body_hash_b64 = b64encode(hashlib.new("md5", raw_body).digest())\
        .decode("utf-8")

    if body_hash_b64 != md5_body:
        raise auth_failed

    hmac_bytes = b64decode(hmac_base64)

    # builds the message
    message_parts = [
        request_method,
        body_hash_b64,
        content_type,
        timestamp,
        path,
    ]

    message = "\n".join(message_parts)

    if __verify_hmac(secret, hmac_bytes, message):
        return True

    raise auth_failed