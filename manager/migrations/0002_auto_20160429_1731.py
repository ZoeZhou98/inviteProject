# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('customer_manager', models.ForeignKey(to=settings.AUTH_USER_MODEL, max_length=32, null=True)),
                ('depart', models.ForeignKey(to='manager.Department', max_length=32, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='third_project',
            name='project_manager',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='third_project',
            name='recruiter',
            field=models.ForeignKey(related_name='recruiters', to=settings.AUTH_USER_MODEL, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='third_project',
            name='customer',
            field=models.ForeignKey(to='manager.Customer', max_length=32, null=True),
        ),
    ]
