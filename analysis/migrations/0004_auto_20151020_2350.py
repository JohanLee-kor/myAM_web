# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0003_amuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amuser',
            name='xing_id',
            field=models.CharField(max_length=10),
        ),
    ]
