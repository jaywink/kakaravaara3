# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_reservation_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='adults',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='children',
        ),
        migrations.AddField(
            model_name='reservableproduct',
            name='pricing_per_person',
            field=models.BooleanField(verbose_name='pricing per person', default=False),
        ),
        migrations.AddField(
            model_name='reservableproduct',
            name='pricing_per_person_included',
            field=models.PositiveIntegerField(blank=True, verbose_name='people included in price', null=True),
        ),
        migrations.AddField(
            model_name='reservableproduct',
            name='pricing_per_person_price',
            field=models.DecimalField(max_digits=6, decimal_places=2, blank=True, verbose_name='price per person', null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='persons',
            field=models.IntegerField(verbose_name='persons', default=1),
        ),
    ]
