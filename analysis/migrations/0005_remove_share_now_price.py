# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_auto_20151020_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='share',
            name='now_price',
        ),
    ]
