# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0011_auto_20160114_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertusersgroups',
            name='g_ID',
        ),
        migrations.AddField(
            model_name='alertusersgroups',
            name='g_class',
            field=models.CharField(primary_key=True, default=b'null', serialize=False, max_length=200, unique=True, verbose_name='\u62a5\u8b66\u7ec4\u7c7b\u522b'),
        ),
        migrations.AddField(
            model_name='alertusersgroups',
            name='g_disturb',
            field=models.CharField(default=b'False', max_length=200, verbose_name='\u662f\u5426\u6253\u6270'),
        ),
    ]
