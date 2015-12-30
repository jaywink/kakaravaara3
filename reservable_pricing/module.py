# -*- coding: utf-8 -*-
import datetime

import six
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from reservable_pricing.models import PeriodPriceModifier
from reservations.utils import get_start_and_end_from_request, get_persons_from_request
from shoop.admin.base import AdminModule, MenuEntry
from shoop.core.models import ShopProduct
from shoop.core.pricing import PriceInfo, PricingContext, PricingModule


class ReservablePricingContext(PricingContext):
    REQUIRED_VALUES = ("start_date", "end_date", "shop")
    shop = None


class ReservablePricingModule(PricingModule):
    identifier = "reservable_pricing"
    name = _("Reservable Pricing")

    pricing_context_class = ReservablePricingContext

    def get_context_from_request(self, request):
        start_date, end_date = get_start_and_end_from_request(request)
        persons = get_persons_from_request(request)

        return self.pricing_context_class(
            shop=request.shop,
            start_date=start_date,
            end_date=end_date,
            persons=persons,
        )

    def get_price_info(self, context, product, quantity=1):
        shop = context.shop

        if isinstance(product, six.integer_types):
            product_id = product
            shop_product = ShopProduct.objects.get(product_id=product_id, shop=shop)
        else:
            shop_product = product.get_shop_instance(shop)
            product_id = product.pk

        base_price = (shop_product.default_price_value or 0) * quantity
        modifiers_price = self.get_modifiers_price(product_id, quantity, context.start_date, context.end_date)
        total_price = base_price + modifiers_price
        total_price = total_price + self.get_per_person_price(product, context.persons) * quantity

        return PriceInfo(
            price=shop.create_price(total_price),
            base_price=shop.create_price(total_price),
            quantity=quantity,
        )

    @staticmethod
    def get_per_person_price(product, persons):
        """Get added price for per person priced reservables."""
        if not product.type.identifier == "reservable" or not persons:
            return 0
        reservable = product.reservable
        if not reservable.pricing_per_person:
            return 0
        difference = max(0, persons - reservable.pricing_per_person_included)
        return difference * reservable.pricing_per_person_price

    @staticmethod
    def get_modifiers_price(product_id, quantity, start_date, end_date):
        """Get amount to add to base price from period modifiers."""
        modifiers_price = 0
        if start_date and end_date:
            # Get any period modifiers that could affect this period
            date_filters = Q(start_date__lte=start_date, end_date__gte=start_date) | \
                           Q(start_date__lte=end_date, end_date__gte=end_date)
            modifiers = PeriodPriceModifier.objects.filter(
                modifier__gt=0, product=product_id
            ).filter(date_filters)
            # Add to the total days * modifier value
            for modifier in modifiers:
                start_from = max(start_date, modifier.start_date)
                # We add +1 day to end because end date is always the *next day*, ie the day guest leaves
                end_on = min(end_date, modifier.end_date + datetime.timedelta(days=1))
                days = min((end_on - start_from).days, quantity)
                modifiers_price += days * modifier.modifier
        return modifiers_price


class PriceModifierModule(AdminModule):
    name = _("Price modifiers")
    category = name

    def get_menu_entries(self, request):
        return [
            MenuEntry(
                text=_("Period"), icon="fa fa-money",
                url="reservable_pricing:modifiers.list",
                category=self.category
            ),
            MenuEntry(
                text=_("Day of Week"), icon="fa fa-money",
                url="reservable_pricing:modifiers.list",
                category=self.category
            ),
        ]
