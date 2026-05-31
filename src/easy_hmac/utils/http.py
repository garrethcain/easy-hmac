import calendar
import datetime
import re


MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()

_D = r"(?P<day>\d{2})"
_D2 = r"(?P<day>[ \d]\d)"
_M = r"(?P<mon>\w{3})"
_Y = r"(?P<year>\d{4})"
_Y2 = r"(?P<year>\d{2})"
_T = r"(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})"

RFC1123_DATE = re.compile(r"^\w{3}, %s %s %s %s GMT$" % (_D, _M, _Y, _T))
RFC850_DATE = re.compile(r"^\w{6,9}, %s-%s-%s %s GMT$" % (_D, _M, _Y2, _T))
ASCTIME_DATE = re.compile(r"^\w{3} %s %s %s %s$" % (_M, _D2, _T, _Y))


def parse_http_date(date: str) -> int:
    """Parse a date format as specified by HTTP RFC7231 section 7.1.1.1.

    Adapted from django.utils.http.

    The three formats allowed by the RFC are accepted, even if only the first
    one is still in widespread use.

    Return an integer expressed in seconds since the epoch, in UTC.
    """
    for regex in RFC1123_DATE, RFC850_DATE, ASCTIME_DATE:
        m = regex.match(date)
        if m is not None:
            break
    else:
        raise ValueError("%r is not in a valid HTTP date format" % date)
    try:
        year = int(m["year"])
        if year < 100:
            current_year = datetime.datetime.now(tz=datetime.timezone.utc).year
            current_century = current_year - (current_year % 100)
            if year - (current_year % 100) > 50:
                year += current_century - 100
            else:
                year += current_century
        _month = MONTHS.index(m["mon"].lower()) + 1
        _day = int(m["day"])
        _hour = int(m["hour"])
        _min = int(m["min"])
        _sec = int(m["sec"])
        result = datetime.datetime(
            year, _month, _day, _hour, _min, _sec, tzinfo=datetime.timezone.utc
        )
        return calendar.timegm(result.utctimetuple())
    except Exception as exc:
        raise ValueError("%r is not a valid date" % date) from exc
