# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-30 18:20
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='未填写标题', max_length=20)),
                ('description', models.TextField(default='未填写描述')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('userLevel', models.PositiveSmallIntegerField(default=0, help_text='用户描述的事件紧急性<br>取值[0,3]', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('userStartTime', models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 5, 52335, tzinfo=utc))),
                ('userEndTime', models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 5, 52335, tzinfo=utc))),
                ('length', models.PositiveIntegerField(default=0, help_text='单位分钟')),
                ('sysStartTime', models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 5, 52335, tzinfo=utc))),
                ('sysEndTime', models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 5, 52335, tzinfo=utc))),
                ('sysLevel', models.PositiveSmallIntegerField(default=0, help_text='系统根据该事件信息及用户日常习惯计算得到的紧急性<br>取值[0,99]', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('state', models.PositiveSmallIntegerField(default=0, help_text='该事务的状态<br>0:等待被安排 1:已安排 2:已取消 3:已完成', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(default='未填写描述', max_length=100)),
                ('useTimes', models.PositiveSmallIntegerField(default=0)),
                ('emergencyLevel', models.PositiveSmallIntegerField(default=20, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('ip', models.GenericIPAddressField(default='127.0.0.1')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(default='未知区域', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('pw', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('isActivated', models.BooleanField()),
                ('activateCode', models.CharField(max_length=6)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_joined', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(default='男', max_length=2)),
                ('weight', models.FloatField(default=0)),
                ('birthday', models.DateTimeField(default=datetime.datetime(2018, 4, 30, 18, 20, 5, 52335, tzinfo=utc))),
                ('age', models.IntegerField(default=0)),
                ('birthplace', models.CharField(default='未填写', max_length=100)),
                ('liveplace', models.CharField(default='未填写', max_length=100)),
                ('userDefault', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.UserDefault')),
            ],
        ),
        migrations.AddField(
            model_name='operationlog',
            name='userDefault',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserDefault'),
        ),
        migrations.AddField(
            model_name='eventtype',
            name='userDefault',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserDefault'),
        ),
        migrations.AddField(
            model_name='event',
            name='eventType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.EventType'),
        ),
        migrations.AddField(
            model_name='event',
            name='userDefault',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserDefault'),
        ),
    ]
