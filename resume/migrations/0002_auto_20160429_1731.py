# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='Turn',
            field=models.SmallIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='Time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 9, 31, 54, 940680, tzinfo=utc)),
        ),
    ]
