from datetime import datetime, timedelta
from shoop.front.basket.objects import BaseBasket
from shoop.front.basket.order_creator import BasketOrderCreator

from reservations.models import Reservation, ReservableProduct


class ReservableBasket(BaseBasket):
    def _compare_line_for_addition(self, current_line_data, product, supplier, shop, extra):
        if product.type.identifier == "reservable":
            # Never add to existing reservation lines
            return False
        return super(
            ReservableBasket, self)._compare_line_for_addition(current_line_data, product, supplier, shop, extra)

    def add_product(self, supplier, shop, product, quantity, force_new_line=False, extra=None, parent_line=None):
        if not extra:
            extra = {}
        if self.request.POST.get("reservation_start", None):
            extra["reservation_start"] = self.request.POST.get("reservation_start")
        return super(ReservableBasket, self).add_product(
            supplier, shop, product, quantity, force_new_line=force_new_line, extra=extra, parent_line=parent_line)


class ReservableOrderCreator(BasketOrderCreator):
    def process_saved_order_line(self, order, order_line):
        if order_line.product and order_line.product.type.identifier == "reservable":
            # Create reservation
            start_date = datetime.strptime(order_line.source_line.get("reservation_start"), "%Y-%m-%d")
            reservable = ReservableProduct.objects.get(product=order_line.product)
            Reservation.objects.create(
                reservable=reservable,
                order=order_line.order,
                start_time=start_date,
                end_time=start_date + timedelta(days=int(order_line.quantity))
            )
            if not order_line.extra_data:
                order_line.extra_data = {}
            order_line.extra_data["reservation_start"] = order_line.source_line.get("reservation_start")
            order_line.save()
