# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='drv_date',
            field=models.DateTimeField(verbose_name='date derived', auto_now=True),
        ),
    ]
