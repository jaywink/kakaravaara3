import datetime
from decimal import Decimal
from unittest.mock import patch

from django.test import RequestFactory
from django.utils.timezone import make_aware

from shoop.core.models import Supplier, AnonymousContact
from shoop.core.pricing import get_pricing_module
from shoop.testing.factories import create_order_with_product

from kakaravaara.tests import KakaravaaraTestsBase
from reservations.basket import ReservableOrderCreator
from reservations.factories import ReservableProductFactory
from reservations.models import Reservation


def get_pricing_context(shop, customer=None):
    return get_pricing_module().get_context_from_data(
        shop=shop,
        customer=(customer or AnonymousContact()),
        start_date=datetime.date(2016, 1, 1),
        end_date=datetime.date(2016, 1, 4),
        persons=3
    )


@patch("shoop.testing.factories._get_pricing_context", new=get_pricing_context)
class ReservableOrderCreatorTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(ReservableOrderCreatorTestCase, self).setUp()
        self.request = RequestFactory().get("/")
        self.reservable = ReservableProductFactory()
        self.roc = ReservableOrderCreator(request=self.request)

    def test_reservation_is_created_with_correct_data(self):
        order = create_order_with_product(self.reservable.product, Supplier.objects.first(), 3, Decimal("100"),
                                          shop=self.shop)
        order_line = order.lines.first()
        order_line.source_line = {
            "reservation_start": datetime.date(2016, 1, 1),
            "persons": 3,
        }
        self.roc.process_saved_order_line(order_line.order, order_line)
        order_line.refresh_from_db()
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.reservable, self.reservable)
        self.assertEqual(reservation.order_line, order_line)
        start_time = make_aware(datetime.datetime.combine(datetime.date(2016, 1, 1), self.reservable.check_in_time))
        self.assertEqual(reservation.start_time, start_time)
        end_time = make_aware(datetime.datetime.combine(datetime.date(2016, 1, 4), self.reservable.check_out_time))
        self.assertEqual(reservation.end_time, end_time)
        self.assertEqual(reservation.persons, 3)
        self.assertEqual(order_line.extra_data["reservation_end"], "2016-01-04")
