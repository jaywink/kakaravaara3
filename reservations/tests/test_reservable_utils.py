import datetime
from unittest import TestCase

from mock import Mock

from reservations.utils import get_start_and_end_from_request


class GetStartAndEndFromRequestTestCase(TestCase):
    def test_dates_returned_from_good_strings(self):
        request = Mock(
            method="POST",
            POST={
                "start": "2016-02-01",
                "end": "2016-02-15",
            }
        )
        start, end = get_start_and_end_from_request(request)
        self.assertEqual(start, datetime.date(2016, 2, 1))
        self.assertEqual(end, datetime.date(2016, 2, 15))

    def test_dates_returned_from_partial_strings(self):
        request = Mock(
            method="POST",
            POST={
                "start": "2016-02",
                "end": "2016-03",
            }
        )
        start, end = get_start_and_end_from_request(request)
        self.assertEqual(start, datetime.date(2016, 2, 1))
        self.assertEqual(end, datetime.date(2016, 3, 1))

    def test_dates_returned_from_good_string_and_days(self):
        request = Mock(
            method="POST",
            POST={
                "start": "2016-02-01",
                "days": "3",
            }
        )
        start, end = get_start_and_end_from_request(request)
        self.assertEqual(start, datetime.date(2016, 2, 1))
        self.assertEqual(end, datetime.date(2016, 2, 4))

    def test_dates_returned_from_good_string_and_quantity(self):
        request = Mock(
            method="POST",
            POST={
                "start": "2016-02-01",
                "quantity": "3",
            }
        )
        start, end = get_start_and_end_from_request(request)
        self.assertEqual(start, datetime.date(2016, 2, 1))
        self.assertEqual(end, datetime.date(2016, 2, 4))
