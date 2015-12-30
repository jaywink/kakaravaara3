from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from shoop.front.checkout.addresses import AddressesPhase, AddressForm
from shoop.front.checkout.confirm import ConfirmPhase, ConfirmForm
from shoop.front.views.checkout import DefaultCheckoutView


class ReservationsCheckoutView(DefaultCheckoutView):
    phase_specs = [
        "reservations.checkout:ReservationsAddressesPhase",
        "reservations.checkout:ReservationsConfirmPhase",
    ]


class ReservationsConfirmForm(ConfirmForm):
    accept_terms = forms.BooleanField(required=True)

    def __init__(self, **kwargs):
        super(ReservationsConfirmForm, self).__init__(**kwargs)
        terms_and_conditions = reverse_lazy("shoop:cms_page", kwargs={"url": "terms"})
        self.fields["accept_terms"].label = mark_safe(_("I have read and agree with the "
                                                      "<a href='%s' target='_blank'>Terms and Conditions</a>")) % (terms_and_conditions)


class ReservationsConfirmPhase(ConfirmPhase):
    form_class = ReservationsConfirmForm


class ReservationsAddressForm(AddressForm):
    def __init__(self, **kwargs):
        super(ReservationsAddressForm, self).__init__(**kwargs)
        self.fields["phone"].required = True
        self.fields["email"].required = True
        self.fields["street"].required = False


class ReservationsAddressesPhase(AddressesPhase):
    address_form_class = ReservationsAddressForm
