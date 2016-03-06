import datetime

from shoop.front.basket.objects import BaseBasket
from shoop.front.basket.order_creator import BasketOrderCreator
from shoop.utils.dates import parse_date

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
        if self.request.POST.get("start", None):
            extra["reservation_start"] = parse_date(self.request.POST.get("start"))
            extra["persons"] = self.request.POST.get("persons", 1)
        # TODO: enable this here once https://github.com/shoopio/shoop/issues/291 is resolved in some way
        # Currently setting `force_new_line` causes product not to be added at all.
        # Once this works, remove above override of `_compare_line_for_addition`.
        # if product.type.identifier == "reservable":
        #     force_new_line = True
        return super(ReservableBasket, self).add_product(
            supplier, shop, product, quantity, force_new_line=force_new_line, extra=extra, parent_line=parent_line)


class ReservableOrderCreator(BasketOrderCreator):
    def process_saved_order_line(self, order, order_line):
        if order_line.product and order_line.product.type.identifier == "reservable":
            # Create reservation
            start_date = order_line.source_line.get("reservation_start")
            reservable = ReservableProduct.objects.get(product=order_line.product)
            start_time = datetime.datetime.combine(start_date, reservable.check_in_time)
            end_date = start_date + datetime.timedelta(days=int(order_line.quantity))
            end_time = datetime.datetime.combine(end_date, reservable.check_out_time)
            Reservation.objects.create(
                reservable=reservable,
                order_line=order_line,
                start_time=start_time,
                end_time=end_time,
                persons=order_line.source_line.get("persons", 1),
            )
            if not order_line.extra_data:
                order_line.extra_data = {}
            order_line.extra_data["reservation_start"] = order_line.source_line.get("reservation_start")
            order_line.extra_data["reservation_end"] = end_date.strftime("%Y-%m-%d")
            order_line.extra_data["persons"] = order_line.source_line.get("persons", 1)
            order_line.save()
