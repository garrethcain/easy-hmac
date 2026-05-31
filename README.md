# easy-hmac

[![PyPI](https://img.shields.io/pypi/v/easy-hmac.svg)](https://pypi.org/project/easy-hmac/)
[![Python](https://img.shields.io/pypi/pyversions/easy-hmac.svg)](https://pypi.org/project/easy-hmac/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A pure Python package with zero dependencies to generate and verify HMAC-SHA256 signatures for HTTP request authentication.

## Installation

```shell
pip install easy-hmac
```

## Quick Start

### Generate a signature

```python
import datetime
import hashlib
import hmac
from base64 import b64encode

from easy_hmac import generate_hmac_sha256

secret = "my-secret-key"
body = '{"event": "updated", "status": "PROCESSING"}'
method = "POST"
path = "/api/v1/webhook"
timestamp = datetime.datetime.now(datetime.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")

digest = generate_hmac_sha256(secret, method, body, path, timestamp)
signature = b64encode(digest).decode()
```

### Verify a signature

```python
from base64 import b64encode, b64decode

from easy_hmac import verify_hmac, AuthenticationFailed

try:
    verify_hmac(
        secret=secret,
        hmac_base64=signature,
        md5_body=content_md5,
        raw_body=body.encode(),
        timestamp=timestamp,
        content_type="application/json",
        path=path,
        request_method=method,
    )
except AuthenticationFailed:
    # Signature invalid, body tampered, or timestamp expired (>15 min)
    pass
```

## API

### `generate_hmac_sha256(secret, method, body, path, timestamp)`

Generates an HMAC-SHA256 digest from HTTP request components.

| Parameter   | Type     | Description                                                       |
|-------------|----------|-------------------------------------------------------------------|
| `secret`    | `str`    | The shared secret key                                             |
| `method`    | `str`    | HTTP method (e.g. `"POST"`)                                       |
| `body`      | `str`    | The request body                                                  |
| `path`      | `str`    | The request path (e.g. `"/api/v1/webhook"`)                       |
| `timestamp` | `str`    | GMT timestamp formatted as `"%a, %d %b %Y %H:%M:%S GMT"`         |

**Returns:** `bytes` — the raw HMAC digest.

### `verify_hmac(secret, hmac_base64, md5_body, raw_body, timestamp, content_type, path, request_method)`

Verifies an incoming HMAC signature against the request components. Checks the body integrity via MD5 hash and rejects requests older than 15 minutes.

| Parameter         | Type     | Description                                                       |
|-------------------|----------|-------------------------------------------------------------------|
| `secret`          | `str`    | The shared secret key                                             |
| `hmac_base64`     | `str`    | The base64-encoded HMAC from the request's Authorization header   |
| `md5_body`        | `str`    | The base64-encoded MD5 hash from the Content-MD5 header           |
| `raw_body`        | `bytes`  | The raw request body                                              |
| `timestamp`       | `str`    | The Date header value                                             |
| `content_type`    | `str`    | The Content-Type header value                                     |
| `path`            | `str`    | The request path                                                  |
| `request_method`  | `str`    | The HTTP method                                                   |

**Returns:** `True` if verification succeeds.

**Raises:** `AuthenticationFailed` if the signature is invalid, the body was tampered, the timestamp is malformed, or the request is older than 15 minutes.

### Exceptions

#### `AuthenticationFailed`

Raised by `verify_hmac` when verification fails. Subclass of `Exception`.

## Message Format

Both functions construct the HMAC message by joining components with newlines:

```
HTTP_METHOD\nCONTENT_MD5\nCONTENT_TYPE\nTIMESTAMP\nPATH
```

This follows a common pattern for REST API HMAC authentication where the content MD5 ensures body integrity and the timestamp prevents replay attacks.

## Development

```shell
# Clone and set up
uv sync

# Run tests
uv run pytest

# Build
uv build
```

## License

[MIT](LICENSE)
