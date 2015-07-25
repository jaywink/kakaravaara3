from datetime import datetime
import pytest
from django.test import TestCase

from reservations.factories import ReservableProductFactory, ReservationFactory
from reservations.models import Reservation


@pytest.mark.django_db
class ReservationsGetReservedDatesTestCase(TestCase):

    def setUp(self):
        super(ReservationsGetReservedDatesTestCase, self).setUp()
        self.reservable = ReservableProductFactory()

    def test_get_reserved_dates_returns_correct_dates(self):
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime(year=2015, month=7, day=5, hour=12)
        )
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime(year=2015, month=7, day=10, hour=12),
            end_time=datetime(year=2015, month=7, day=15, hour=12)
        )
        dates = self.reservable.get_reserved_dates(
            start=datetime(year=2015, month=5, day=1),
            end=datetime(year=2015, month=8, day=1)
        )
        self.assertEquals(len(dates), 10)

    def test_get_reserved_dates_for_period_returns_correct_dates(self):
        self.reservable2 = ReservableProductFactory()
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime(year=2015, month=7, day=5, hour=12)
        )
        ReservationFactory(
            reservable=self.reservable2,
            start_time=datetime(year=2015, month=7, day=10, hour=12),
            end_time=datetime(year=2015, month=7, day=15, hour=12)
        )
        dates = Reservation.get_reserved_days_for_period(
            start_time=datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime(year=2015, month=7, day=15, hour=12)
        )
        self.assertEquals(len(dates), 10)

    def test_is_period_free(self):
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime(year=2015, month=6, day=30, hour=15),
            end_time=datetime(year=2015, month=7, day=5, hour=12)
        )
        ReservationFactory(
            reservable=self.reservable,
            start_time=datetime(year=2015, month=7, day=10, hour=12),
            end_time=datetime(year=2015, month=7, day=15, hour=12)
        )
        self.assertFalse(self.reservable.is_period_free(
            datetime(year=2015, month=6, day=27, hour=15),
            datetime(year=2015, month=7, day=3, hour=12)
        ))
        self.assertTrue(self.reservable.is_period_free(
            datetime(year=2015, month=6, day=27, hour=15),
            datetime(year=2015, month=6, day=29, hour=12)
        ))
        self.assertTrue(self.reservable.is_period_free(
            datetime(year=2015, month=6, day=27, hour=15),
            datetime(year=2015, month=6, day=30, hour=12)
        ))
