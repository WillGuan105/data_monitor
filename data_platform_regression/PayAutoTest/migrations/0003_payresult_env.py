# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('PayAutoTest', '0002_payresult_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='payresult',
            name='env',
            field=models.CharField(default=datetime.datetime(2015, 9, 18, 4, 18, 37, 210237, tzinfo=utc), max_length=200, verbose_name='\u6267\u884c\u73af\u5883'),
            preserve_default=False,
        ),
    ]
