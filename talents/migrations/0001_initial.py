# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Examine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Result', models.CharField(max_length=12, blank=True)),
                ('Time', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('Is_resultful', models.SmallIntegerField(null=True, blank=True)),
                ('Count', models.SmallIntegerField(null=True, blank=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_5', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PositionName', models.CharField(max_length=100)),
                ('Phone1', models.CharField(max_length=11, null=True, blank=True)),
                ('ExistingPersonNum', models.IntegerField(null=True, blank=True)),
                ('NeedPersonNum', models.IntegerField(null=True, blank=True)),
                ('recruitednum', models.IntegerField(default=0, null=True, blank=True)),
                ('Workplace', models.CharField(max_length=32, null=True, blank=True)),
                ('ProjectName', models.CharField(max_length=32, null=True, blank=True)),
                ('LoWSalary', models.IntegerField(null=True, blank=True)),
                ('HighSalary', models.IntegerField(null=True, blank=True)),
                ('Headline', models.DateTimeField(null=True)),
                ('RecruitReason', models.SmallIntegerField(null=True, blank=True)),
                ('RecruitTime', models.CharField(max_length=100, null=True, blank=True)),
                ('WorkContent', models.TextField(null=True, blank=True)),
                ('CandidateRequirement', models.TextField(null=True)),
                ('RecruitWay', models.SmallIntegerField(null=True, blank=True)),
                ('States', models.CharField(default=b'\xe6\x9c\xaa\xe5\xa4\x84\xe7\x90\x86', max_length=12, null=True, blank=True)),
                ('Accept', models.SmallIntegerField(null=True, blank=True)),
                ('Awarding', models.IntegerField(null=True, blank=True)),
                ('Email', models.EmailField(default=b'si_zhaopin@nantian.com.cn', max_length=254, blank=True)),
                ('Filing', models.SmallIntegerField(default=2, blank=True)),
                ('Salary', models.CharField(max_length=32, null=True, blank=True)),
                ('add_reason', models.TextField(null=True, blank=True)),
                ('pub_time', models.DateTimeField(null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
                ('Approver', models.ForeignKey(related_name='Position_Approver', to=settings.AUTH_USER_MODEL, null=True)),
                ('Depart', models.ForeignKey(to='manager.Department', null=True)),
                ('SecondDepartment', models.ForeignKey(related_name='Position_SecondDepartment', to='manager.Department', null=True)),
                ('UserID', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='examine',
            name='PositionID',
            field=models.ForeignKey(to='talents.Position'),
        ),
        migrations.AddField(
            model_name='examine',
            name='UserID',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='examine',
            name='last_user',
            field=models.ForeignKey(related_name='Examine_last_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='examine',
            name='next_approver',
            field=models.ForeignKey(related_name='Examine_next_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
