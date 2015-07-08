from datetime import date, timedelta

from datetimewidget.widgets import DateWidget

from django.forms import forms, DateField
from django.utils.translation import ugettext as _


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
