# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservableProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('check_out_time', models.TimeField(verbose_name='sign out time')),
                ('check_in_time', models.TimeField(verbose_name='sign in time')),
                ('available_count', models.IntegerField(verbose_name='available quantity', default=1)),
                ('product', models.OneToOneField(verbose_name='reservable product', to='shoop.Product', related_name='reservable')),
            ],
            options={
                'verbose_name_plural': 'reservable products',
                'verbose_name': 'reservable product',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('start_time', models.DateTimeField(verbose_name='starts')),
                ('end_time', models.DateTimeField(verbose_name='ends')),
                ('adults', models.IntegerField(verbose_name='adults', default=1)),
                ('children', models.IntegerField(verbose_name='children', default=0)),
                ('reservable', models.ForeignKey(verbose_name='reservable product', to='reservations.ReservableProduct', related_name='reservations')),
            ],
            options={
                'verbose_name_plural': 'reservations',
                'verbose_name': 'reservation',
            },
        ),
    ]
