# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobid', models.CharField(max_length=200, verbose_name='\u5de5\u5355\u53f7')),
                ('result', models.CharField(max_length=200, verbose_name='\u8fd0\u884c\u7ed3\u679c')),
            ],
        ),
    ]
