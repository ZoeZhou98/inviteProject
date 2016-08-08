# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('talents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='fail_import_id',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=32, null=True)),
                ('resume_id', models.CharField(max_length=32, null=True)),
                ('source', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
                ('referrerID', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='import_ID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=32, null=True)),
                ('resume_id', models.CharField(max_length=32, null=True)),
                ('source', models.CharField(max_length=32, null=True)),
                ('Time', models.DateTimeField(auto_now=True)),
                ('Status', models.SmallIntegerField(default=0, null=True)),
                ('remark', models.TextField(null=True, blank=True)),
                ('UploaderID', models.ForeignKey(related_name='import_UploaderID', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='importid_group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('remark', models.TextField(null=True, blank=True)),
                ('Status', models.SmallIntegerField(default=0, null=True)),
                ('DepartID', models.ForeignKey(blank=True, to='manager.Department', null=True)),
                ('PositionID', models.ForeignKey(blank=True, to='talents.Position', null=True)),
                ('referrerID', models.ForeignKey(related_name='import_referrerID', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('userID', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mail_Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Ename', models.CharField(max_length=32, null=True, blank=True)),
                ('Ephone', models.CharField(max_length=32, null=True, blank=True)),
                ('Email', models.CharField(max_length=32, null=True, blank=True)),
                ('Eentrytime', models.CharField(max_length=32, null=True, blank=True)),
                ('Epost', models.CharField(max_length=32, null=True, blank=True)),
                ('Epostgrade', models.CharField(max_length=32, null=True, blank=True)),
                ('Ejob', models.CharField(max_length=32, null=True, blank=True)),
                ('Ejobin', models.CharField(max_length=32, null=True, blank=True)),
                ('Ejobaim', models.CharField(max_length=32, null=True, blank=True)),
                ('Eprimary', models.CharField(max_length=32, null=True, blank=True)),
                ('Esecond', models.CharField(max_length=32, null=True, blank=True)),
                ('Eproject', models.CharField(max_length=32, null=True, blank=True)),
                ('Ecompacttime', models.CharField(max_length=32, null=True, blank=True)),
                ('Eapplytime', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_1', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_2', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_3', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_4', models.CharField(max_length=32, null=True, blank=True)),
                ('handletime', models.DateTimeField(auto_now_add=True, null=True)),
                ('handleuser', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repeat_Resume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=32, null=True)),
                ('resume_phone', models.CharField(max_length=32, null=True)),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
                ('referrerID', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SearchID', models.CharField(max_length=32, null=True)),
                ('PositionName', models.CharField(max_length=128, null=True)),
                ('CandidateName', models.CharField(max_length=32, null=True)),
                ('CandidateSex', models.CharField(max_length=4, null=True)),
                ('CandidateAge', models.CharField(max_length=11, null=True)),
                ('CandidatePhone', models.CharField(max_length=11, null=True)),
                ('CandidateEmail', models.EmailField(max_length=32, null=True)),
                ('CandidateProfile', models.IntegerField(null=True, blank=True)),
                ('Candidate_edu', models.CharField(max_length=20, null=True)),
                ('Addr', models.CharField(max_length=64)),
                ('Status', models.CharField(default=b'\xe6\x9c\xaa\xe5\xa4\x84\xe7\x90\x86', max_length=20, editable=False)),
                ('Level', models.SmallIntegerField(null=True, blank=True)),
                ('Time', models.DateTimeField(default=datetime.datetime(2016, 4, 20, 3, 28, 30, 581760, tzinfo=utc))),
                ('Notes', models.CharField(max_length=128, null=True, blank=True)),
                ('lastinter', models.CharField(max_length=32, null=True, blank=True)),
                ('LockTime', models.DateTimeField(null=True, blank=True)),
                ('temp_2', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_3', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_4', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_5', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_6', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_7', models.CharField(max_length=32, null=True, blank=True)),
                ('Agency', models.ForeignKey(related_name='Resume_Agency', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('NextUser', models.ManyToManyField(related_name='Resume_NextUser', to=settings.AUTH_USER_MODEL, blank=True)),
                ('Station', models.ForeignKey(related_name='Resume_Station', blank=True, to='talents.Position', null=True)),
                ('UserID', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('referrerID', models.ForeignKey(related_name='Resume_referrerID', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='mail_offer',
            name='resume',
            field=models.ForeignKey(blank=True, to='resume.Resume', null=True),
        ),
        migrations.AddField(
            model_name='import_id',
            name='groupid',
            field=models.ForeignKey(blank=True, to='resume.importid_group', null=True),
        ),
        migrations.AddField(
            model_name='import_id',
            name='referrerID',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
