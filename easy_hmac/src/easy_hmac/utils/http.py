# Code adapted from from django.utils.http.py
import re
import datetime
import calendar


# list of months
MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()

# two digit day: 22, 10, 01, 02, etc
__D = r"(?P<day>\d{2})"

# also two digit day: 25, 01, etc
__D2 = r"(?P<day>[ \d]\d)"

# month: jan, fev, mar...
__M = r"(?P<mon>\w{3})"

# year, 4 digits: 1995, 2021
__Y = r"(?P<year>\d{4})"

# year, 2 digits: 95, 87
__Y2 = r"(?P<year>\d{2})"

# Timestamp
__T = r"(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})"


# first three characters are the name of the day: Mon, Tue, Wed, Thu, Fri, Sat,
# Sun ex: Sun, 06 Nov 1994 08:49:37 GMT
RFC1123_DATE = re.compile(r"^\w{3}, %s %s %s %s GMT$" % (__D, __M, __Y, __T))

# here the day name can be Monday, Tuesday, Wednesday, Thursday, Saturday, 
# Sunday hence \w{6,9} in the beginning
# ex: Sunday, 06-Nov-94 08:49:37 GMT
RFC850_DATE = re.compile(r"^\w{6,9}, %s-%s-%s %s GMT$" % (__D, __M, __Y2, __T))

# ex: Sun Nov  6 08:49:37 1994
ASCTIME_DATE = re.compile(r"^\w{3} %s %s %s %s$" % (__M, __D2, __T, __Y))


def parse_http_date(date: str) -> int:
    # TODO: parse_http_date is originaly from django.utils.http.py
    """
    Note: this code is originally from django.utils.http.py
    Parse a date format as specified by HTTP RFC7231 section 7.1.1.1.

    The three formats allowed by the RFC are accepted, even if only the first
    one is still in widespread use.

    Return an integer expressed in seconds since the epoch, in UTC.
    """
    # email.utils.parsedate() does the job for RFC1123 dates; unfortunately
    # RFC7231 makes it mandatory to support RFC850 dates too. So we roll
    # our own RFC-compliant parsing.
    for regex in RFC1123_DATE, RFC850_DATE, ASCTIME_DATE:
        m = regex.match(date)
        if m is not None:
            break
    else:
        raise ValueError("%r is not in a valid HTTP date format" % date)
    try:
        year = int(m["year"])
        if year < 100:
            current_year = datetime.datetime.now(datetime.timezone.utc).year
            current_century = current_year - (current_year % 100)
            if year - (current_year % 100) > 50:
                # year that appears to be more than 50 years in the future are
                # interpreted as representing the past.
                year += current_century - 100
            else:
                year += current_century
        _month = MONTHS.index(m["mon"].lower()) + 1
        _day = int(m["day"])
        _hour = int(m["hour"])
        _min = int(m["min"])
        _sec = int(m["sec"])
        result = datetime.datetime(year, _month, _day, _hour, _min, _sec)
        return calendar.timegm(result.utctimetuple())
    except Exception as exc:
        raise ValueError("%r is not a valid date" % date) from exc
