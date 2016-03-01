# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('PayAutoTest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payresult',
            name='author',
            field=models.CharField(default=datetime.datetime(2015, 8, 31, 1, 57, 41, 747662, tzinfo=utc), max_length=200, verbose_name='\u6267\u884c\u4eba'),
            preserve_default=False,
        ),
    ]
