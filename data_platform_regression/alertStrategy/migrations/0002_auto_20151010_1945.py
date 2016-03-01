# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertrecord',
            name='a_lastMsgTimes',
            field=models.DateTimeField(null=True, verbose_name='\u4e0a\u4e00\u6b21\u77ed\u4fe1\u62a5\u8b66\u53d1\u9001\u65f6\u95f4', blank=True),
        ),
    ]
