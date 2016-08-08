# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resume', '__first__'),
        ('talents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Cname', models.CharField(max_length=32, null=True, blank=True)),
                ('Ctype', models.CharField(max_length=32, null=True, blank=True)),
                ('Creason', models.CharField(max_length=32, null=True, blank=True)),
                ('Ctime', models.DateTimeField(auto_now_add=True, null=True)),
                ('Cnotes', models.CharField(max_length=64, null=True, blank=True)),
                ('temp_1', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_2', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_3', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_4', models.CharField(max_length=32, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handletime', models.DateTimeField(auto_now_add=True, null=True)),
                ('touser', models.CharField(max_length=32, null=True, blank=True)),
                ('Type', models.CharField(max_length=32, null=True, blank=True)),
                ('notes', models.CharField(max_length=32, null=True, blank=True)),
                ('cc', models.TextField(null=True, blank=True)),
                ('bcc', models.TextField(null=True, blank=True)),
                ('handleuser', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('EntryResults', models.TextField()),
                ('Time', models.DateTimeField(null=True, blank=True)),
                ('temp_1', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_2', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_3', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_4', models.CharField(max_length=32, null=True, blank=True)),
                ('handletime', models.DateTimeField(auto_now_add=True, null=True)),
                ('position', models.ForeignKey(blank=True, to='talents.Position', null=True)),
                ('resume', models.ForeignKey(blank=True, to='resume.Resume', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HandleRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handletime', models.DateTimeField(auto_now_add=True, null=True)),
                ('Type', models.CharField(max_length=32, null=True, blank=True)),
                ('active', models.SmallIntegerField(default=1, null=True, blank=True)),
                ('notes', models.CharField(max_length=32, null=True, blank=True)),
                ('handleuser', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('InterviewResults', models.TextField()),
                ('Level', models.SmallIntegerField(null=True, blank=True)),
                ('Time', models.DateTimeField(null=True, blank=True)),
                ('InterviewProcess', models.CharField(default=b'\xe6\x9c\xaa\xe5\xa4\x84\xe7\x90\x86', max_length=20, null=True, blank=True)),
                ('InterStatus', models.CharField(default=b'\xe6\x9c\xaa\xe5\xa4\x84\xe7\x90\x86', max_length=20, null=True, blank=True)),
                ('Notes', models.CharField(max_length=100, null=True, blank=True)),
                ('Active', models.SmallIntegerField(default=1, null=True, blank=True)),
                ('temp_1', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_2', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_3', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_4', models.CharField(max_length=32, null=True, blank=True)),
                ('handletime', models.DateTimeField(auto_now_add=True, null=True)),
                ('Agency', models.ForeignKey(related_name='Interview_Agency', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('NextUser', models.ManyToManyField(related_name='Interview_NextUser', to=settings.AUTH_USER_MODEL, blank=True)),
                ('lockuser', models.ForeignKey(related_name='Interview_lockuser', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('resume', models.ForeignKey(blank=True, to='resume.Resume', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Iaddr', models.CharField(max_length=32, null=True, blank=True)),
                ('Itime', models.CharField(max_length=32, null=True, blank=True)),
                ('Iname', models.CharField(max_length=32, null=True, blank=True)),
                ('Iphone', models.CharField(max_length=32, null=True, blank=True)),
                ('Imail', models.CharField(max_length=32, null=True, blank=True)),
                ('Inotes', models.CharField(max_length=64, null=True, blank=True)),
                ('temp_1', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_2', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_3', models.CharField(max_length=32, null=True, blank=True)),
                ('temp_4', models.CharField(max_length=32, null=True, blank=True)),
                ('handletime', models.DateTimeField(auto_now_add=True, null=True)),
                ('handleuser', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('interview', models.ForeignKey(blank=True, to='side.Interview', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='handlerecord',
            name='interview',
            field=models.ForeignKey(blank=True, to='side.Interview', null=True),
        ),
        migrations.AddField(
            model_name='handlerecord',
            name='resume',
            field=models.ForeignKey(blank=True, to='resume.Resume', null=True),
        ),
        migrations.AddField(
            model_name='emailrecord',
            name='interview',
            field=models.ForeignKey(blank=True, to='side.Interview', null=True),
        ),
        migrations.AddField(
            model_name='emailrecord',
            name='resume',
            field=models.ForeignKey(blank=True, to='resume.Resume', null=True),
        ),
        migrations.AddField(
            model_name='changerecord',
            name='interview',
            field=models.ForeignKey(blank=True, to='side.Interview', null=True),
        ),
    ]
