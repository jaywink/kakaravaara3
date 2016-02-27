# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_auto_20151227_2203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservableproduct',
            options={'verbose_name_plural': 'reservable products', 'ordering': ('sort_order',), 'verbose_name': 'reservable product'},
        ),
        migrations.AddField(
            model_name='reservableproduct',
            name='sort_order',
            field=models.PositiveIntegerField(default=50, verbose_name='sort order'),
        ),
    ]
