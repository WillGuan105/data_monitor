# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('PayAutoTest', '0003_payresult_env'),
    ]

    operations = [
        migrations.AddField(
            model_name='payresult',
            name='ctime',
            field=models.CharField(default=datetime.datetime(2015, 9, 29, 8, 57, 59, 373028, tzinfo=utc), max_length=200, verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payresult',
            name='etime',
            field=models.CharField(default=datetime.datetime(2015, 9, 29, 8, 58, 6, 391011, tzinfo=utc), max_length=200, verbose_name='\u7ed3\u675f\u65f6\u95f4'),
            preserve_default=False,
        ),
    ]
