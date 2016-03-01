# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0004_auto_20151021_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoritems',
            name='m_active',
            field=models.CharField(default=True, max_length=200, verbose_name='\u662f\u5426\u53ef\u7528'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='monitoritems',
            name='m_params',
            field=models.CharField(max_length=500, verbose_name='\u8bf7\u6c42\u53c2\u6570'),
        ),
    ]
