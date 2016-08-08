# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_auto_20160429_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='Time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 9, 37, 24, 960932, tzinfo=utc)),
        ),
    ]
