from django.forms import ModelForm
from shoop.admin.form_part import FormPart, TemplatedFormDef

from reservations.models import ReservableProduct


class ReservableProductForm(ModelForm):

    class Meta:
        model = ReservableProduct
        fields = (
            "pricing_per_person",
            "pricing_per_person_included",
            "pricing_per_person_price",
            "sort_order",
            "check_out_time",
            "check_in_time",
            # "available_count",  # not implemented yet
        )


class ReservableProductFormPart(FormPart):
    priority = -980

    def _get_reservable_instance(self):
        if hasattr(self.object, "reservable"):
            return self.object.reservable
        else:
            reservable, created = ReservableProduct.objects.get_or_create(product=self.object)
            return reservable

    def get_form_defs(self):
        yield TemplatedFormDef(
            "reservableproduct",
            ReservableProductForm,
            template_name="reservations/_reservable_product_form.jinja",
            required=True,
            kwargs={
                "instance": self._get_reservable_instance(),
            }
        )

    def form_valid(self, form):
        try:
            form["reservableproduct"].save()
        except KeyError:
            pass
