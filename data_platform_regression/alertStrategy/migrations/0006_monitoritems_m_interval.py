# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0005_auto_20151026_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoritems',
            name='m_interval',
            field=models.IntegerField(default=1, help_text=b'\xe4\xbb\xa5min\xe4\xb8\xba\xe5\x8d\x95\xe4\xbd\x8d,\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba1', verbose_name='\u4efb\u52a1\u8fd0\u884c\u9891\u7387'),
        ),
    ]
