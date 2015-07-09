# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0001_initial'),
        ('reservations', '0002_auto_20150709_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='order',
            field=models.ForeignKey(null=True, verbose_name='order', to='shoop.Order', related_name='reservations', blank=True),
        ),
    ]
