# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_auto_20160429_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='Time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 9, 49, 47, 893002, tzinfo=utc)),
        ),
    ]
