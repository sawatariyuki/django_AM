# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-30 18:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='sysEndTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 44, 270578, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='sysStartTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 44, 270578, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='userEndTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 44, 270578, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='userStartTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 44, 270578, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 44, 270578, tzinfo=utc)),
        ),
    ]
