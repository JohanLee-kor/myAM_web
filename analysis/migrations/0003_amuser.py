# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_auto_20151018_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='AMuser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('am_id', models.CharField(max_length=10)),
                ('am_pass', models.CharField(max_length=30)),
                ('account_number', models.CharField(max_length=14)),
                ('account_pw', models.CharField(max_length=4)),
                ('xing_id', models.CharField(max_length=4)),
                ('xing_pass', models.CharField(max_length=8)),
                ('xing_certificate_pass', models.CharField(max_length=10)),
            ],
        ),
    ]
