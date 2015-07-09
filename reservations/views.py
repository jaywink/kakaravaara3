from shoop.admin.modules.products.views import ProductEditView
from shoop.front.views.product import ProductDetailView

from reservations.forms import ReservableDatesForm, ReservedDatesFormPart


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


class ReservableProductEditView(ProductEditView):

    def get_form_part_classes(self):
        form_part_classes = super(ReservableProductEditView, self).get_form_part_classes()
        if self.object.type.identifier == "reservable":
            form_part_classes.append(ReservedDatesFormPart)

        return form_part_classes
