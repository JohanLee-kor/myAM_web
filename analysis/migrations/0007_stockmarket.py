# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0006_share_now_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockMarket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gubun', models.CharField(max_length=1)),
                ('hname', models.CharField(max_length=20)),
                ('pricejisu', models.IntegerField(default=0)),
                ('jniljisu', models.IntegerField(default=0)),
                ('sign', models.IntegerField(default=-1)),
                ('change', models.IntegerField(default=-1)),
                ('diffjisu', models.IntegerField(default=-1)),
                ('volume', models.IntegerField(default=-1)),
                ('jnilvolume', models.IntegerField(default=-1)),
                ('volumechage', models.IntegerField(default=-1)),
                ('volumerate', models.IntegerField(default=-1)),
                ('market_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
