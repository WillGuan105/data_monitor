# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0010_auto_20160113_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoritems',
            name='m_alertGroupID',
        ),
        migrations.AlterField(
            model_name='monitoritems',
            name='m_alertUsers',
            field=models.CharField(max_length=200, verbose_name='\u62a5\u8b66\u63a5\u6536\u4eba(\u7ec4)'),
        ),
    ]
