from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from shoop.front.checkout.confirm import ConfirmPhase, ConfirmForm
from shoop.front.views.checkout import DefaultCheckoutView


class ReservationsCheckoutView(DefaultCheckoutView):
    phase_specs = [
        "shoop.front.checkout.addresses:AddressesPhase",
        "reservations.checkout:ReservationsConfirmPhase",
    ]


class ReservationsConfirmForm(ConfirmForm):
    accept_terms = forms.BooleanField(required=True)

    def __init__(self, **kwargs):
        super(ReservationsConfirmForm, self).__init__(**kwargs)
        terms_and_conditions = reverse_lazy("shoop:cms_page", kwargs={"url": "terms"})
        self.fields["accept_terms"].label = mark_safe(_("I have read and agree with the "
                                                      "<a href='%s'>Terms and Conditions</a>")) % (terms_and_conditions)


class ReservationsConfirmPhase(ConfirmPhase):
    form_class = ReservationsConfirmForm
