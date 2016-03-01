# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smokeTest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interface',
            name='i_params',
            field=models.CharField(max_length=500, verbose_name='\u8bf7\u6c42\u53c2\u6570'),
        ),
    ]
