# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckDiffItems',
            fields=[
                ('c_ID', models.IntegerField(unique=True, serialize=False, verbose_name='\u68c0\u6d4b\u540c\u5546\u54c1\u63a5\u53e3id', primary_key=True)),
                ('c_active', models.CharField(max_length=200, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('c_name', models.CharField(max_length=200, verbose_name='\u540d\u5b57')),
                ('c_baseurl', models.CharField(max_length=200, verbose_name='\u8bf7\u6c42url http://')),
                ('c_params', models.CharField(max_length=500, verbose_name='\u8bf7\u6c42\u53c2\u6570')),
                ('c_host', models.CharField(max_length=200, verbose_name='host -H "host:"')),
                ('c_path', models.CharField(max_length=200, verbose_name='\u81f3twitter_id\u8def\u5f84')),
            ],
        ),
    ]
