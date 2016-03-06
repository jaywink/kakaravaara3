import datetime

from django.test import RequestFactory
from django.utils.timezone import make_aware
from mock import Mock
from shoop.testing.factories import create_empty_order, get_default_shop

from kakaravaara.tests import KakaravaaraTestsBase
from reservations.basket import ReservableOrderCreator
from reservations.factories import ReservableProductFactory
from reservations.models import Reservation


class MockOrderLine(Mock):
    def __init__(self, product, quantity, reservation_start, persons):
        super(MockOrderLine, self).__init__()
        self.product = product
        self.quantity = quantity
        self.source_line = {
            "reservation_start": reservation_start,
            "persons": persons,
        }
        self.order = create_empty_order(shop=get_default_shop()).save()
        self.extra_data = {}
        self.save_called = False

    def save(self):
        self.save_called = True


class ReservableOrderCreatorTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(ReservableOrderCreatorTestCase, self).setUp()
        self.request = RequestFactory().get("/")
        self.reservable = ReservableProductFactory()
        self.roc = ReservableOrderCreator(request=self.request)

    def test_reservation_is_created_with_correct_data(self):
        mock_order_line = MockOrderLine(self.reservable.product, 3, datetime.date(2016, 1, 1), 3)
        self.roc.process_saved_order_line(Mock(), mock_order_line)
        self.assertTrue(mock_order_line.save_called)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.reservable, self.reservable)
        self.assertEqual(reservation.order, mock_order_line.order)
        start_time = make_aware(datetime.datetime.combine(datetime.date(2016, 1, 1), self.reservable.check_in_time))
        self.assertEqual(reservation.start_time, start_time)
        end_time = make_aware(datetime.datetime.combine(datetime.date(2016, 1, 4), self.reservable.check_out_time))
        self.assertEqual(reservation.end_time, end_time)
        self.assertEqual(reservation.persons, 3)
        self.assertEqual(mock_order_line.extra_data["reservation_end"], "2016-01-04")

