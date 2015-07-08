from shoop.front.views.product import ProductDetailView
from reservations.forms import ReservableDatesForm


class ReservableProductDetailView(ProductDetailView):

    def get_context_data(self, **kwargs):
        context = super(ReservableProductDetailView, self).get_context_data(**kwargs)

        if self.object.type.identifier == "reservable":
            # Add form for date inputs
            context["reservable_dates_form"] = ReservableDatesForm()

        return context

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if product.type.identifier == "reservable":
            # Use our template for reservables
            self.template_name = "reservations/reservable_product.jinja"

        return super(ReservableProductDetailView, self).get(request, *args, **kwargs)
