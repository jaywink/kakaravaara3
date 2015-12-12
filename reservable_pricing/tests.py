import datetime

from django.test import RequestFactory

from kakaravaara.tests import KakaravaaraTestsBase
from reservable_pricing.factories import PeriodPriceModifierFactory
from reservations.factories import ReservableProductFactory
from shoop.core.models import ShopProduct


class ReservablePricingModulePeriodModifiersTestCase(KakaravaaraTestsBase):

    def setUp(self):
        super(ReservablePricingModulePeriodModifiersTestCase, self).setUp()
        self.reservable = ReservableProductFactory()
        self.product = self.reservable.product
        self.modifier = PeriodPriceModifierFactory(product=self.product)
        # Verify factories
        assert self.modifier.start_date == datetime.date(2015, 11, 1)
        assert self.modifier.end_date == datetime.date(2015, 11, 30)
        self.request = RequestFactory().get("/")
        self.request.shop = self.shop

    def test_get_price_info_returns_correct_price_with_no_modifiers(self):
        shop_product = ShopProduct.objects.get(product=self.reservable.product, shop=self.shop)
        self.assertEqual(self.reservable.product.get_price(
            self.request, quantity=2).value, shop_product.default_price_value * 2
        )

    def test_get_price_info_returns_correct_price_with_dates_outside_modifiers(self):
        shop_product = ShopProduct.objects.get(product=self.reservable.product, shop=self.shop)
        self.request.GET = {
            "start": "2015-10-01",
            "end": "2015-10-03",
        }
        self.assertEqual(
            self.reservable.product.get_price(self.request, quantity=2).value, shop_product.default_price_value * 2
        )

    def test_get_price_info_returns_correct_price_with_modifiers(self):
        shop_product = ShopProduct.objects.get(product=self.reservable.product, shop=self.shop)
        self.request.GET = {
            "start": "2015-11-01",
            "end": "2015-11-03",
        }
        expected_price = shop_product.default_price_value * 2 + self.modifier.modifier * 2
        self.assertEqual(self.reservable.product.get_price(self.request, quantity=2).value, expected_price)

    def test_get_price_info_returns_correct_price_with_start_before_modifiers(self):
        shop_product = ShopProduct.objects.get(product=self.reservable.product, shop=self.shop)
        self.request.GET = {
            "start": "2015-10-30",
            "end": "2015-11-02",
        }
        expected_price = shop_product.default_price_value * 3 + self.modifier.modifier
        self.assertEqual(self.reservable.product.get_price(self.request, quantity=3).value, expected_price)

    def test_get_price_info_returns_correct_price_with_end_after_modifiers(self):
        shop_product = ShopProduct.objects.get(product=self.reservable.product, shop=self.shop)
        self.request.GET = {
            "start": "2015-11-30",
            "end": "2015-12-03",
        }
        expected_price = shop_product.default_price_value * 3 + self.modifier.modifier
        self.assertEqual(self.reservable.product.get_price(self.request, quantity=3).value, expected_price)
