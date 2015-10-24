# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('analysis_type', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=10)),
                ('init_price', models.IntegerField(default=0)),
                ('now_price', models.IntegerField(default=0)),
                ('drv_date', models.DateTimeField(verbose_name='date derived')),
            ],
        ),
    ]
