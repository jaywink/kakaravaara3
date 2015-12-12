# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservable_pricing', '0004_auto_20151213_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodpricemodifier',
            name='product',
            field=models.ForeignKey(related_name='period_price_modifiers', to='shoop.Product'),
        ),
    ]
