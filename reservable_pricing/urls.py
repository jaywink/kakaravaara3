from django.conf.urls import url, patterns

from reservable_pricing.views import PeriodPricingModifierListView, PeriodPricingModifierEditView


urlpatterns = patterns(
    '',
    url(r"^sa/pricing/modifiers/period/(?P<pk>\d+)/$",
        PeriodPricingModifierEditView.as_view(), name="modifiers.period.edit"),
    url(r"^sa/pricing/modifiers/period/new/$",
        PeriodPricingModifierEditView.as_view(), name="modifiers.period.new"),
    url(r"^sa/pricing/modifiers/period/",
        PeriodPricingModifierListView.as_view(), name="modifiers.period.list"),
    url(r"^sa/pricing/modifiers/dow/(?P<pk>\d+)/$",
        DoWPricingModifierEditView.as_view(), name="modifiers.dow.edit"),
    url(r"^sa/pricing/modifiers/dow/new/$",
        DoWPricingModifierEditView.as_view(), name="modifiers.dow.new"),
    url(r"^sa/pricing/modifiers/dow/",
        DoWPricingModifierListView.as_view(), name="modifiers.dow.list"),
)
