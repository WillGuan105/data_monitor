# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='alertRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a_ID', models.IntegerField(unique=True, verbose_name='\u62a5\u8b66\u63a5\u53e3id')),
                ('a_InterfaceName', models.CharField(max_length=200, verbose_name='\u63a5\u53e3\u540d\u5b57')),
                ('a_createTime', models.DateTimeField(verbose_name='\u62a5\u8b66\u8bb0\u5f55\u521b\u5efa\u65f6\u95f4')),
                ('a_mailTimes', models.IntegerField(default=0, verbose_name='\u62a5\u8b66\u90ae\u4ef6\u53d1\u9001\u6b21\u6570')),
                ('a_msgTimes', models.IntegerField(default=0, verbose_name='\u62a5\u8b66\u77ed\u4fe1\u53d1\u9001\u6b21\u6570')),
                ('a_lastMsgTimes', models.DateTimeField(verbose_name='\u4e0a\u4e00\u6b21\u77ed\u4fe1\u62a5\u8b66\u53d1\u9001\u65f6\u95f4', blank=True)),
            ],
        ),
    ]
