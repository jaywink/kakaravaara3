from babel.dates import format_date
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from reservable_pricing.models import PeriodPriceModifier
from shoop.admin.toolbar import URLActionButton
from shoop.admin.utils.picotable import Column, TextFilter
from shoop.admin.utils.views import PicotableListView, CreateOrUpdateView
from shoop.utils.i18n import get_current_babel_locale


class PeriodPricingModifierListView(PicotableListView):
    model = PeriodPriceModifier
    columns = [
        Column(
            "name", _("Name"), sort_field="product__translations__name",
            display="product__name",
            filter_config=TextFilter(
                filter_field="product__translations__name",
                placeholder=_("Filter by product..."))
        ),
        Column("start_date", _("Start date"), sort_field="start_date", display="format_start_date"),
        Column("end_date", _("End date"), sort_field="end_date", display="format_end_date"),
        Column("modifier", _(u"Modifier"), sort_field="modifier"),
    ]

    def format_start_date(self, instance, *args, **kwargs):
        return format_date(instance.start_date, locale=get_current_babel_locale())

    def format_end_date(self, instance, *args, **kwargs):
        return format_date(instance.end_date, locale=get_current_babel_locale())

    def get_toolbar(self):
        toolbar = super(PeriodPricingModifierListView, self).get_toolbar()
        toolbar.append(URLActionButton(
            text=_("New modifier"),
            icon="fa fa-money",
            url=reverse("reservable_pricing:modifiers.new"),
        ))
        return toolbar

    def get_object_url(self, instance):
        return reverse(
            "reservable_pricing:modifiers.edit", kwargs={"pk": instance.id})


class PeriodPriceModifierForm(ModelForm):
    class Meta:
        model = PeriodPriceModifier
        exclude = ()


class PeriodPricingModifierEditView(CreateOrUpdateView):
    model = PeriodPriceModifier
    template_name = "reservable_pricing/period_modifier_edit.jinja"
    context_object_name = "period_modifier"
    form_class = PeriodPriceModifierForm
