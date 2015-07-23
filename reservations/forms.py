from django.forms import ModelForm
from shoop.admin.form_part import FormPart, TemplatedFormDef

from reservations.models import ReservableProduct


class ReservableProductForm(ModelForm):

    class Meta:
        model = ReservableProduct
        fields = (
            "check_out_time",
            "check_in_time",
            "available_count",
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

    def get_initial(self):
        pass
