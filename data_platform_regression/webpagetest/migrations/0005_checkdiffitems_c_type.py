# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpagetest', '0004_auto_20151207_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkdiffitems',
            name='c_type',
            field=models.CharField(default=b'["null"]', max_length=200, verbose_name='\u5e73\u53f0\u7c7b\u578b\uff08pc\u6216mob\uff09'),
        ),
    ]
