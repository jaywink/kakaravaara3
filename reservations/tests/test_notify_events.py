from mock import Mock

from kakaravaara.tests import KakaravaaraTestsBase
from reservations.notify_events import get_order_details


class LinesMock(Mock):
    def filter(self, type=None):
        return [Mock(
            text="Cool cottage",
            product=Mock(
                type=Mock(
                    identifier="reservable"
                )
            ),
            extra_data={
                "reservation_start": "2016-01-01",
                "persons": 3,
            },
            quantity=4,
        )]


class GetOrderDetailsForNotifyEventsTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(GetOrderDetailsForNotifyEventsTestCase, self).setUp()
        self.order = Mock(
            lines=LinesMock()
        )

    def test_correct_string_is_returned(self):
        self.assertEqual(
            get_order_details(self.order),
            "Cool cottage\n"
            "    4 nights, 3 persons, 2016-01-01 - 2016-01-05"
        )
