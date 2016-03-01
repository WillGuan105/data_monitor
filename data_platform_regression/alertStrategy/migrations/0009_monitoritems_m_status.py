# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0008_auto_20151110_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoritems',
            name='m_status',
            field=models.CharField(default=b'not useful', max_length=200, verbose_name='\u5f53\u524d\u72b6\u6001'),
        ),
    ]
