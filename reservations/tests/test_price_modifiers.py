import datetime
from decimal import Decimal

from django.test import RequestFactory
from shoop.core.models import ShopProduct, AnonymousContact

from kakaravaara.tests import KakaravaaraTestsBase
from reservable_pricing.factories import PeriodPriceModifierFactory
from reservations.factories import ReservableProductFactory


class ReservablePricePerPersonTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(ReservablePricePerPersonTestCase, self).setUp()
        self.request = RequestFactory().get("/")
        self.request.GET = {"persons": 3}
        self.request.shop = self.shop
        self.request.customer = AnonymousContact()
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


class ReservableHasPriceModifiersTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(ReservableHasPriceModifiersTestCase, self).setUp()
        self.reservable = ReservableProductFactory()
        self.tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.yesterday = datetime.date.today() - datetime.timedelta(days=1)

    def test_reservable_has_no_modifiers(self):
        self.assertFalse(self.reservable.has_price_modifiers)

    def test_reservable_has_per_person_modifier(self):
        self.reservable.pricing_per_person = True
        self.reservable.save()
        self.assertTrue(self.reservable.has_price_modifiers)

    def test_reservable_has_period_price_modifiers(self):
        PeriodPriceModifierFactory(
            product=self.reservable.product, start_date=self.tomorrow, end_date=self.tomorrow)
        self.assertTrue(self.reservable.has_price_modifiers)

    def test_reservable_has_only_passed_period_price_modifiers(self):
        PeriodPriceModifierFactory(
            product=self.reservable.product, start_date=self.yesterday, end_date=self.yesterday)
        self.assertFalse(self.reservable.has_price_modifiers)
