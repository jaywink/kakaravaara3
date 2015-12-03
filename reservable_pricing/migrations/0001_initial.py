# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import shoop.utils.properties
import shoop.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0012_add_configurations'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservableProductPrice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('price_value', shoop.core.fields.MoneyValueField(max_digits=36, decimal_places=9)),
                ('group', models.ForeignKey(to='shoop.ContactGroup')),
                ('product', models.ForeignKey(to='shoop.Product', related_name='+')),
                ('shop', models.ForeignKey(to='shoop.Shop')),
            ],
            options={
                'verbose_name': 'product price',
                'verbose_name_plural': 'product prices',
            },
            bases=(shoop.utils.properties.MoneyPropped, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='reservableproductprice',
            unique_together=set([('product', 'shop', 'group')]),
        ),
    ]
