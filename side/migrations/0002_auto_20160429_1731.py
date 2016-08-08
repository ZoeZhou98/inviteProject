# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('side', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='Projectname',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='interview',
            name='Turn',
            field=models.SmallIntegerField(null=True, blank=True),
        ),
    ]
