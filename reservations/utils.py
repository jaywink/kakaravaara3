import re
from datetime import timedelta

from shoop.utils.dates import parse_date


def expand_datestring_without_day(date):
    """Expand date string YYYY-MM with day.

    For example; 2016-02 will become 2016-02-01.

    Args:
        string - Date string that will be checked.
    Returns:
        string - Expanded date string with "-01" appended, or original given string.
    """
    if re.match("^[0-9]{4}-[0-9]{2}$", date):
        return "%s-01" % date
    return date


def get_start_and_end_from_request(request):
    """Get start and end dates from request.

    Returns:
        date, date or None, None
    """
    start = getattr(request, request.method).get("start", None)
    if start:
        start = expand_datestring_without_day(start)
    end = getattr(request, request.method).get("end", None)
    if end:
        end = expand_datestring_without_day(end)
    if "days" in getattr(request, request.method):
        days = getattr(request, request.method).get("days", None)
    else:
        days = getattr(request, request.method).get("quantity", None)
    if start and (end or days):
        start_date = parse_date(start)
        if end:
            end_date = parse_date(end)
        else:
            end_date = start_date + timedelta(days=int(days))
    else:
        return None, None
    return start_date, end_date


def get_persons_from_request(request):
    """Get person count from request.

    Returns:
        int
    """
    persons = int(getattr(request, request.method).get("persons", 1))
    return persons


def daterange(start_date, end_date):
    """Taken from http://stackoverflow.com/a/1060330/1489738."""
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
