import datetime

from kakaravaara.tests import KakaravaaraTestsBase
from reservations.factories import ReservableProductFactory, ReservationFactory
from reservations.models import Reservation


class ReservationsGetReservedDatesTestCase(KakaravaaraTestsBase):

    def setUp(self):
        super(ReservationsGetReservedDatesTestCase, self).setUp()
        self.reservable = ReservableProductFactory()

    def test_get_reserved_dates_returns_correct_dates(self):
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime.datetime(year=2015, month=7, day=5, hour=12)
        )
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime(year=2015, month=7, day=10, hour=12),
            end_time=datetime.datetime(year=2015, month=7, day=15, hour=12)
        )
        dates = self.reservable.get_reserved_dates(
            start=datetime.date(year=2015, month=5, day=1),
            end=datetime.date(year=2015, month=8, day=1)
        )
        self.assertEquals(len(dates), 10)

    def test_get_reserved_dates_for_period_returns_correct_dates(self):
        self.reservable2 = ReservableProductFactory()
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime.datetime(year=2015, month=7, day=5, hour=12)
        )
        ReservationFactory(
            reservable=self.reservable2,
            start_time=datetime.datetime(year=2015, month=7, day=10, hour=12),
            end_time=datetime.datetime(year=2015, month=7, day=15, hour=12)
        )
        dates = Reservation.get_reserved_days_for_period(
            start_date=datetime.date(year=2015, month=6, day=30),
            end_date=datetime.date(year=2015, month=7, day=15)
        )
        self.assertEquals(len(dates), 10)

    def test_get_reserved_dates_for_period_returns_correct_dates__spanning_months(self):
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime.datetime(year=2015, month=8, day=5, hour=12)
        )
        dates = Reservation.get_reserved_days_for_period(
            start_date=datetime.date(year=2015, month=7, day=15),
            end_date=datetime.date(year=2015, month=7, day=20)
        )
        self.assertEquals(len(dates), 6)

    def test_is_period_free(self):
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime.datetime(year=2015, month=7, day=5, hour=12)
        )
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime(year=2015, month=7, day=10, hour=12),
            end_time=datetime.datetime(year=2015, month=7, day=15, hour=12)
        )
        self.assertFalse(self.reservable.is_period_days_free(
            datetime.date(year=2015, month=6, day=27),
            datetime.date(year=2015, month=7, day=3)
        ))
        self.assertTrue(self.reservable.is_period_days_free(
            datetime.date(year=2015, month=6, day=27),
            datetime.date(year=2015, month=6, day=29)
        ))
        self.assertTrue(self.reservable.is_period_days_free(
            datetime.date(year=2015, month=6, day=27),
            datetime.date(year=2015, month=6, day=30)
        ))
