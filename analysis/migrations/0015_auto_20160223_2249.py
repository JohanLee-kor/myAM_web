# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0014_auto_20160223_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='drv_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date derived'),
        ),
    ]
