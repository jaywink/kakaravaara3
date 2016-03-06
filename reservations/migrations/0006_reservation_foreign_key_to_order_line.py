# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0014_verbose_names'),
        ('reservations', '0005_add_sort_order_to_reservableproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='order',
        ),
        migrations.AddField(
            model_name='reservation',
            name='order_line',
            field=models.OneToOneField(related_name='reservation', to='shoop.OrderLine', verbose_name='order line', null=True, blank=True),
        ),
    ]
