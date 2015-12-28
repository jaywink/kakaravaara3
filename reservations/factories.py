# -*- coding: utf-8 -*-
from datetime import time, datetime
import factory

from shoop.core.models import ProductType
from shoop.testing.factories import ProductFactory

from reservations.models import Reservation, ReservableProduct


class ReservableProductProductFactory(ProductFactory):
    @factory.lazy_attribute
    def type(self):
        return ProductType.objects.get_or_create(identifier="reservable")[0]


class ReservableProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = ReservableProduct

    product = factory.SubFactory(ReservableProductProductFactory)
    check_out_time = time(hour=12)
    check_in_time = time(hour=15)


class ReservationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Reservation

    reservable = factory.SubFactory(ReservableProductFactory)
    start_time = datetime(year=2015, month=6, day=30, hour=15)
    end_time = datetime(year=2015, month=7, day=5, hour=12)
