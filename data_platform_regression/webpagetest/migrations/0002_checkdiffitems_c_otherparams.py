# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpagetest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkdiffitems',
            name='c_otherparams',
            field=models.CharField(default=b'["null"]', max_length=200, verbose_name='\u5176\u4ed6\u9700\u8981\u89e3\u6790\u7684json\u5217\u8868\uff08\u5982\u5206\u9875\u7b49\uff09'),
        ),
    ]
