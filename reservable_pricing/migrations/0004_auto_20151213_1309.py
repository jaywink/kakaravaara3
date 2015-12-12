# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservable_pricing', '0003_auto_20151213_1306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='periodpricemodifier',
            old_name='modifier_value',
            new_name='modifier',
        ),
    ]
