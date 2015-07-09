from datetime import date, timedelta

from datetimewidget.widgets import DateWidget
from django.conf import settings
from django.forms import forms, DateField, ModelForm
from django.utils.translation import ugettext as _

from shoop.admin.form_part import FormPart, TemplatedFormDef
from shoop.utils.multilanguage_model_form import to_language_codes

from reservations.models import ReservableProduct

DATEPICKER_OPTIONS = {
    "weekStart": 1,
    "minView": 2,
    "maxView": 3,
    "clearBtn": False,
}


class ReservableDatesForm(forms.Form):
    start_date = DateField(
        label=_("Start date"),
        required=True,
        initial=date.today(),
        widget=DateWidget(
            attrs={'id':"reservable-start-date"}, usel10n=True, bootstrap_version=3, options=DATEPICKER_OPTIONS,
        )
    )

    end_date = DateField(
        label=_("End date"),
        required=True,
        initial=date.today() + timedelta(days=1),
        widget=DateWidget(
            attrs={'id':"reservable-end-date"}, usel10n=True, bootstrap_version=3, options=DATEPICKER_OPTIONS
        )
    )


class ReservedDatesForm(forms.Form):
    def __init__(self, **kwargs):
        super(ReservedDatesForm, self).__init__()
        self.languages = to_language_codes(kwargs.pop("languages", ()))
        self.product = kwargs.pop("product")
        self.reservations = self.product.reservable.reservations.all()

    def cleaned_data(self):
        return None

    def save(self):
        pass


class ReservedDatesFormPart(FormPart):
    priority = -950

    def get_form_defs(self):
        yield TemplatedFormDef(
            "reservations",
            ReservedDatesForm,
            template_name="reservations/_reserved_dates_form.jinja",
            required=True,
            kwargs={
                "product": self.object,
                "languages": settings.LANGUAGES,
                "initial": self.get_initial()
            }
        )

    def get_initial(self):
        pass


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
