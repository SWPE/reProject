# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 12:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_importantinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='importantinfo',
            name='hash',
            field=models.CharField(default=datetime.datetime(2017, 11, 26, 12, 27, 33, 302893, tzinfo=utc), max_length=500),
            preserve_default=False,
        ),
    ]
