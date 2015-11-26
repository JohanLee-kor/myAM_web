# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0005_remove_share_now_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='now_price',
            field=models.IntegerField(default=0),
        ),
    ]
