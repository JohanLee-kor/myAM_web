# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0013_auto_20160223_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='drv_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 22, 46, 22, 367000), verbose_name='date derived'),
        ),
    ]
