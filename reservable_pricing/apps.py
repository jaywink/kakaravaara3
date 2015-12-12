# -*- coding: utf-8 -*-
from shoop.apps import AppConfig


class ReservablePricingAppConfig(AppConfig):
    name = "reservable_pricing"
    verbose_name = "Reservable Pricing"
    label = "reservable_pricing"
    provides = {
        "pricing_module": [
            "reservable_pricing.module:ReservablePricingModule"
        ],
        "admin_module": [
            "reservable_pricing.module:PriceModifierModule"
        ],
    }
