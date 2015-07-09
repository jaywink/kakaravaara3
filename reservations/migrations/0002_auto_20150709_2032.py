# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservableproduct',
            name='check_in_time',
            field=models.TimeField(verbose_name='sign in time', default=datetime.time(15, 0)),
        ),
        migrations.AlterField(
            model_name='reservableproduct',
            name='check_out_time',
            field=models.TimeField(verbose_name='sign out time', default=datetime.time(12, 0)),
        ),
    ]
