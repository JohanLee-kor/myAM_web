# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0009_auto_20151129_0058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockmarket',
            old_name='volumechage',
            new_name='volumechange',
        ),
    ]
