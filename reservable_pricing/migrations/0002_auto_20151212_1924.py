# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import shoop.core.fields
import shoop.utils.properties


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0012_add_configurations'),
        ('reservable_pricing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodPriceModifier',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('modifier_value', shoop.core.fields.MoneyValueField(decimal_places=9, max_digits=36)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('product', models.ForeignKey(related_name='+', to='shoop.Product')),
                ('shop', models.ForeignKey(to='shoop.Shop')),
            ],
            options={
                'verbose_name_plural': 'period price modifiers',
                'verbose_name': 'period price modifier',
            },
            bases=(shoop.utils.properties.MoneyPropped, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='reservableproductprice',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='reservableproductprice',
            name='group',
        ),
        migrations.RemoveField(
            model_name='reservableproductprice',
            name='product',
        ),
        migrations.RemoveField(
            model_name='reservableproductprice',
            name='shop',
        ),
        migrations.DeleteModel(
            name='ReservableProductPrice',
        ),
        migrations.AlterUniqueTogether(
            name='periodpricemodifier',
            unique_together=set([('product', 'shop', 'start_date', 'end_date')]),
        ),
    ]
