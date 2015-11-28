# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0007_stockmarket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockmarket',
            name='gubun',
        ),
        migrations.RemoveField(
            model_name='stockmarket',
            name='hname',
        ),
    ]
