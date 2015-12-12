# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservable_pricing', '0002_auto_20151212_1924'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='periodpricemodifier',
            unique_together=set([('product', 'start_date', 'end_date')]),
        ),
        migrations.RemoveField(
            model_name='periodpricemodifier',
            name='shop',
        ),
    ]
