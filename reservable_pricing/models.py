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
