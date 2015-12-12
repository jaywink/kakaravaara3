# -*- coding: utf-8 -*-
import datetime

import factory
from factory.fuzzy import FuzzyDecimal

from reservable_pricing.models import PeriodPriceModifier
from shoop.testing.factories import ProductFactory


class PeriodPriceModifierFactory(factory.DjangoModelFactory):
    class Meta:
        model = PeriodPriceModifier

    product = factory.SubFactory(ProductFactory)
    modifier = FuzzyDecimal(1, 200)
    start_date = datetime.date(2015, 11, 1)
    end_date = datetime.date(2015, 11, 30)
