from shoop.front.basket.objects import BaseBasket


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
