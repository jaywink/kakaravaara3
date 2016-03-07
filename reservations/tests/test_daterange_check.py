import datetime
from decimal import Decimal

from dateutil import relativedelta
from django.core.urlresolvers import reverse
from django.test import RequestFactory

from reservations.factories import ReservableProductFactory, ReservationFactory
from reservations.tests.test_reservable_views import ReservableViewsBaseTestCase
from shoop.utils.i18n import format_money


class DateRangeCheckViewTestCase(ReservableViewsBaseTestCase):
    def setUp(self):
        super(DateRangeCheckViewTestCase, self).setUp()
        self.reservable = ReservableProductFactory()
        self.reservation = ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime.today(),
            end_time=datetime.datetime.today() + datetime.timedelta(days=3)
        )
        self.today = datetime.date.today()
        self.next = datetime.date.today() + relativedelta.relativedelta(months=1)

    def test_view_returns_bad_request_on_missing_parameters(self):
        response = self.client.get(reverse('reservations:check_period'))
        self.assertEqual(response.status_code, 400)
        url = "%s?reservable_id=1" % reverse('reservations:check_period')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        url = "%s?start=2015-10-01" % reverse('reservations:check_period')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        url = "%s?end=2015-10-01" % reverse('reservations:check_period')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_free_period_should_return_period_is_free(self):
        request = RequestFactory().get("/")
        request.shop = self.shop
        response = self.client.get(
            "%s?reservable_id=%s&start=%s&end=%s" % (
                reverse('reservations:check_period'),
                self.reservable.id,
                self.next.strftime("%Y-%m-%d"),
                (self.next + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
            )
        )
        price_info = self.reservable.product.get_price_info(request, quantity=3)
        self.assertJSONEqual(response.content.decode("utf-8"), {
            "result": True,
            "price": {
                "total": format_money(price_info.price),
                "has_extra_info": False,
            }
        })

    def test_free_period_should_return_period_is_free_and_extra_info(self):
        request = RequestFactory().get("/")
        request.GET = {"persons": 3}
        request.shop = self.shop
        self.reservable.pricing_per_person = True
        self.reservable.pricing_per_person_included = 2
        self.reservable.pricing_per_person_price = Decimal("10.00")
        self.reservable.save()
        response = self.client.get(
            "%s?reservable_id=%s&start=%s&end=%s&persons=3" % (
                reverse('reservations:check_period'),
                self.reservable.id,
                self.next.strftime("%Y-%m-%d"),
                (self.next + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
            )
        )
        price_info = self.reservable.product.get_price_info(request, quantity=3)
        self.assertJSONEqual(response.content.decode("utf-8"), {
            "result": True,
            "price": {
                "total": format_money(price_info.price),
                "period_modifiers": str(price_info.period_modifiers.quantize(Decimal("1.00"))),
                "per_person_modifiers": str(price_info.per_person_modifiers.quantize(Decimal("1.00"))),
                "has_extra_info": True,
                "special_period_str": "Special period",
                "persons_count_str": "Person count",
            }
        })

    def test_reserved_period_should_return_period_is_reserved(self):
        response = self.client.get(
            "%s?reservable_id=%s&start=%s&end=%s" % (
                reverse('reservations:check_period'),
                self.reservable.id,
                self.today.strftime("%Y-%m-%d"),
                (self.today + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
            )
        )
        self.assertJSONEqual(response.content.decode("utf-8"), {
            "result": False,
            "price": None,
        })
