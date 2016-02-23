# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0010_auto_20151130_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='drv_date',
            field=models.DateTimeField(verbose_name='date derived', auto_now_add=True),
        ),
    ]
