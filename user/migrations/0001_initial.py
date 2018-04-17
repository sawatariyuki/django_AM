# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-15 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('pw', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('isActivated', models.BooleanField()),
                ('activateCode', models.CharField(max_length=6)),
            ],
        ),
    ]