# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-08 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_eventtype_isdeleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipaddress',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='last_used',
            field=models.DateTimeField(auto_now=True),
        ),
    ]