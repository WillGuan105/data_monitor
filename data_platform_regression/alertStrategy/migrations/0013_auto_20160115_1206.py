# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0012_auto_20160115_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoritems',
            name='m_alertUsers',
            field=models.CharField(max_length=200, verbose_name='\u62a5\u8b66\u63a5\u6536\u4eba', blank=True),
        ),
    ]
