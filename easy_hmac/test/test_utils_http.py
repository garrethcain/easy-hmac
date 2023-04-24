# Test suite for easy_hmac
from easy_hmac.utils.http import parse_http_date
import unittest


class TestUtilsHTTP(unittest.TestCase):
    """
    Houses the tests for the easy_hmac.utils.http
    """

    def test_parse_http_date_wrong_date_format(self):
        """
        Tests if a date on a format not accepted by parse_http_date
        raises a ValueError exception
        """
        wrong_date = "Monday, 14/12/2021 - 10:47:23"
        self.assertRaises(ValueError, parse_http_date, wrong_date)

    def test_parse_http_date_RFC1123(self):
        """
        Given a date on the RFC1123 format, tests if it correctly parses to epoch
        Epoch value, 784111777, was given by https://www.epochconverter.com/
        """
        RFC1123 = "Sun, 06 Nov 1994 08:49:37 GMT"
        actual = parse_http_date(RFC1123)
        self.assertEqual(784111777, actual)

    def test_parse_http_date_RFC850(self):
        """
        Given a date on the RFC850 format, tests if it correctly parses to epoch
        Epoch value, 784111777, was given by https://www.epochconverter.com/
        """
        RFC850_date = "Sunday, 06-Nov-94 08:49:37 GMT"
        actual = parse_http_date(RFC850_date)
        self.assertEqual(784111777, actual)

    def test_parse_http_date_ASCII(self):
        """
        Given a date on the ASCII format, tests if it correctly parses to epoch
        Epoch value, 784111777, was given by https://www.epochconverter.com/
        """
        ASCII_date = "Sun Nov  6 08:49:37 1994"
        actual = parse_http_date(ASCII_date)
        self.assertEqual(784111777, actual)


if __name__ == "__main__":
    unittest.main()
