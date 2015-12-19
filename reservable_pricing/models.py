# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from shoop.core.fields import MoneyValueField
from shoop.utils.properties import MoneyPropped


class PeriodPriceModifier(MoneyPropped, models.Model):
    product = models.ForeignKey("shoop.Product", related_name="period_price_modifiers", on_delete=models.CASCADE)
    modifier = MoneyValueField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = (("product", "start_date", "end_date"))
        verbose_name = _(u"period price modifier")
        verbose_name_plural = _(u"period price modifiers")

    def __repr__(self):
        return "<PeriodPriceModifier (%s, %s, %s, %s)" % (
            self.product_id,
            self.start_date.strftime(settings.SHORT_DATE_FORMAT),
            self.end_date.strftime(settings.SHORT_DATE_FORMAT),
            self.modifier,
        )


DAYS_OF_WEEK = (
    (0, _("Monday")),
    (1, _("Tuesday")),
    (2, _("Wednesday")),
    (3, _("Thursday")),
    (4, _("Friday")),
    (5, _("Saturday")),
    (6, _("Sunday")),
)


class DoWPriceModifier(MoneyPropped, models.Model):
    product = models.ForeignKey("shoop.Product", related_name="dow_price_modifiers", on_delete=models.CASCADE)
    modifier = MoneyValueField()
    dow = models.CharField(choices=DAYS_OF_WEEK)

    class Meta:
        unique_together = (("product", "dow"))
        verbose_name = _(u"dow price modifier")
        verbose_name_plural = _(u"dow price modifiers")

    def __repr__(self):
        return "<DoWPriceModifier (%s, %s, %s)" % (
            self.product_id,
            self.get_dow_display(),
            self.modifier,
        )
