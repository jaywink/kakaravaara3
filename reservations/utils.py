from datetime import datetime, timedelta


def get_start_and_end_from_request(request):
    """Get start and end dates from request.

    Returns:
        date, date or None, None
    """
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    days = request.GET.get("days", None)
    if start and (end or days):
        start_date = datetime.strptime(start, "%Y-%m")
        if end:
            end_date = datetime.strptime(end, "%Y-%m")
        else:
            end_date = start_date + timedelta(days=int(days))
    else:
        return None, None
    return start_date.date(), end_date.date()


def daterange(start_date, end_date):
    """Taken from http://stackoverflow.com/a/1060330/1489738."""
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
