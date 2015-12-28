# -*- coding: utf-8 -*-
from datetime import time, datetime
import factory
from shoop.testing.factories import ProductFactory, ProductTypeFactory

from reservations.models import Reservation, ReservableProduct


class ReservableProductTypeFactory(ProductTypeFactory):
    identifier = "reservable"


class ReservableProductProductFactory(ProductFactory):
    type = factory.SubFactory(ReservableProductTypeFactory)


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
