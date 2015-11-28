# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_auto_20151129_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmarket',
            name='gubun',
            field=models.CharField(default='0', max_length=1),
        ),
        migrations.AddField(
            model_name='stockmarket',
            name='hname',
            field=models.CharField(default=datetime.datetime(2015, 11, 28, 15, 58, 27, 537000, tzinfo=utc), max_length=20),
            preserve_default=False,
        ),
    ]
