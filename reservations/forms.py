from datetime import date, timedelta

from datetimewidget.widgets import DateWidget
from django.conf import settings
from django.forms import forms, DateField
from django.utils.translation import ugettext as _

from shoop.admin.form_part import FormPart, TemplatedFormDef
from shoop.utils.multilanguage_model_form import to_language_codes

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
