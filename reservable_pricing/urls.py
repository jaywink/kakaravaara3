from django.conf.urls import url, patterns

from reservable_pricing.views import PeriodPricingModifierListView, PeriodPricingModifierEditView


urlpatterns = patterns(
    '',
    url(r"^sa/pricing/modifiers/period/(?P<pk>\d+)/$",
        PeriodPricingModifierEditView.as_view(), name="modifiers.edit"),
    url(r"^sa/pricing/modifiers/period/new/$",
        PeriodPricingModifierEditView.as_view(), name="modifiers.new"),
    url(r"^sa/pricing/modifiers/period/",
        PeriodPricingModifierListView.as_view(), name="modifiers.list"),
)
