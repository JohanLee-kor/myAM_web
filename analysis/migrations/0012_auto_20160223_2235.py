# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0011_auto_20160223_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='drv_date',
            field=models.DateTimeField(verbose_name='date derived', default=datetime.datetime(2016, 2, 23, 22, 35, 58, 568000)),
        ),
    ]
