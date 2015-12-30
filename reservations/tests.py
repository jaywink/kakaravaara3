import datetime
from decimal import Decimal

from dateutil import relativedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory
from django.utils.translation import activate
from shoop.core.models import ShopProduct

from kakaravaara.tests import KakaravaaraTestsBase
from reservations.factories import ReservableProductFactory, ReservationFactory
from reservations.models import Reservation
from shoop.xtheme.theme import set_current_theme


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


class ReservableViewsBaseTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(ReservableViewsBaseTestCase, self).setUp()
        activate("en")
        set_current_theme("shoop_simple_theme")
        self.client = Client()


class ReservableSearchViewTestCase(ReservableViewsBaseTestCase):
    def setUp(self):
        super(ReservableSearchViewTestCase, self).setUp()
        self.reservable = ReservableProductFactory()
        self.reservation = ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime.today(),
            end_time=datetime.datetime.today() + datetime.timedelta(days=3)
        )
        self.response = self.client.get(reverse('reservations:reservable.search'))
        self.today = datetime.date.today()
        self.next = datetime.date.today() + relativedelta.relativedelta(months=1)

    def test_view_responds(self):
        self.assertContains(self.response, u"Select months to search from")

    def test_context_data(self):
        context = self.response.context_data
        self.assertEqual(list(context["reservables"]), [self.reservable])
        self.assertEqual(context["start_month"], self.today.strftime("%m/%Y"))
        self.assertEqual(context["end_month"], self.next.strftime("%m/%Y"))
        self.assertEqual(
            context["start_date"],
            (self.today + relativedelta.relativedelta(day=1)).strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(
            context["end_date"],
            (self.today + relativedelta.relativedelta(day=1, months=+2, days=-1)).strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(context["reserved_days"], {
            self.reservable.product.sku: [
                self.today.strftime("%Y-%m-%d"),
                (self.today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                (self.today + datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            ]
        })
        self.assertEqual(context["visible_attributes"], settings.RESERVABLE_SEARCH_VISIBLE_ATTRIBUTES)
        self.assertEqual(
            context["months"],
            [
                self.today.strftime("%Y-%m"),
                (self.today + relativedelta.relativedelta(months=1)).strftime("%Y-%m"),
            ]
        )


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
        self.assertJSONEqual(response.content.decode("utf-8"), {
            "result": True,
            "price": {
                "total": str((self.reservable.product.get_price(request) * 3).quantize(Decimal("1.00"))),
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


class ReservablePricePerPersonTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(ReservablePricePerPersonTestCase, self).setUp()
        self.request = RequestFactory().get("/")
        self.request.GET = {"persons": 3}
        self.request.shop = self.shop
        self.reservable = ReservableProductFactory(
            pricing_per_person_included=0, pricing_per_person_price=Decimal("10.00"),
        )

    def test_reservable_with_pricing_per_person_disabled_person_count_doesnt_change_price(self):
        self.reservable.pricing_per_person = False
        self.reservable.save()
        price = self.reservable.product.get_price(self.request, quantity=1).quantize(Decimal("1.00"))
        shop_product = ShopProduct.objects.get(product_id=self.reservable.product_id, shop=self.shop)
        self.assertEqual(price, shop_product.default_price)

    def test_reservable_with_pricing_per_person_active_person_count_changes_price(self):
        self.reservable.pricing_per_person = True
        self.reservable.save()
        price = self.reservable.product.get_price(self.request, quantity=1).quantize(Decimal("1.00"))
        shop_product = ShopProduct.objects.get(product_id=self.reservable.product_id, shop=self.shop)
        self.assertAlmostEqual(price.value, shop_product.default_price_value + 3 * Decimal("10.00"), 6)

    def test_reservable_with_pricing_per_person_active_person_count_changes_price_more_nights(self):
        self.reservable.pricing_per_person = True
        self.reservable.save()
        price = self.reservable.product.get_price(self.request, quantity=3).quantize(Decimal("1.00"))
        shop_product = ShopProduct.objects.get(product_id=self.reservable.product_id, shop=self.shop)
        self.assertAlmostEqual(price.value, shop_product.default_price_value * 3 + 3 * Decimal("10.00") * 3, 6)

    def test_reservable_with_pricing_per_person_included_count_zero(self):
        self.reservable.pricing_per_person = True
        self.reservable.save()
        price = self.reservable.product.get_price(self.request, quantity=1).quantize(Decimal("1.00"))
        shop_product = ShopProduct.objects.get(product_id=self.reservable.product_id, shop=self.shop)
        self.assertAlmostEqual(price.value, shop_product.default_price_value + 3 * Decimal("10.00"), 6)

    def test_reservable_with_pricing_per_person_included_count_above_zero(self):
        self.reservable.pricing_per_person = True
        self.reservable.pricing_per_person_included = 2
        self.reservable.save()
        price = self.reservable.product.get_price(self.request, quantity=1).quantize(Decimal("1.00"))
        shop_product = ShopProduct.objects.get(product_id=self.reservable.product_id, shop=self.shop)
        self.assertAlmostEqual(price.value, shop_product.default_price_value + Decimal("10.00"), 6)
