# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fakecube', '0002_auto_20150730_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='fakecubeif',
            name='f_status',
            field=models.CharField(default='', max_length=200, verbose_name='\u8fd0\u884c\u7ed3\u679c\u72b6\u6001'),
            preserve_default=False,
        ),
    ]
