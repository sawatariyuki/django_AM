# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-17 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180417_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefault',
            name='pw',
            field=models.CharField(max_length=50),
        ),
    ]
