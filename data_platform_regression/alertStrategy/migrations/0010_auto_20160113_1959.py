# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0009_monitoritems_m_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='alertUsersGroups',
            fields=[
                ('g_ID', models.IntegerField(unique=True, serialize=False, verbose_name='\u62a5\u8b66\u7ec4id', primary_key=True)),
                ('g_name', models.CharField(max_length=200, verbose_name='\u540d\u5b57')),
                ('g_alertUsers', models.CharField(max_length=200, verbose_name='\u62a5\u8b66\u63a5\u6536\u7ec4\u6210\u5458')),
            ],
        ),
        migrations.AddField(
            model_name='monitoritems',
            name='m_alertGroupID',
            field=models.CharField(max_length=200, null=True, verbose_name='\u62a5\u8b66\u63a5\u6536\u7ec4id', blank=True),
        ),
        migrations.AlterField(
            model_name='monitoritems',
            name='m_alertUsers',
            field=models.CharField(max_length=200, verbose_name='\u62a5\u8b66\u63a5\u6536\u4eba', blank=True),
        ),
    ]
