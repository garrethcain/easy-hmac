import pytest

from easy_hmac.utils.http import parse_http_date


def test_parse_http_date_wrong_date_format():
    with pytest.raises(ValueError):
        parse_http_date("Monday, 14/12/2021 - 10:47:23")


def test_parse_http_date_rfc1123():
    assert parse_http_date("Sun, 06 Nov 1994 08:49:37 GMT") == 784111777


def test_parse_http_date_rfc850():
    assert parse_http_date("Sunday, 06-Nov-94 08:49:37 GMT") == 784111777


def test_parse_http_date_asctime():
    assert parse_http_date("Sun Nov  6 08:49:37 1994") == 784111777
