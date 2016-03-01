# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0002_auto_20151010_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='alertReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r_interfaceName', models.CharField(max_length=200, verbose_name='\u63a5\u53e3\u540d\u5b57')),
                ('r_class', models.CharField(max_length=200, verbose_name='\u63a5\u53e3\u6240\u5c5e\u7c7b\u522bGroupon,focus,data')),
                ('r_plat', models.CharField(max_length=200, verbose_name='\u5e73\u53f0pc,mob')),
                ('r_city', models.CharField(max_length=200, verbose_name='\u57ce\u5e02\u5317\u4eac,\u5e7f\u5dde')),
                ('r_createTime', models.DateTimeField(verbose_name='\u62a5\u8b66\u8bb0\u5f55\u521b\u5efa\u65f6\u95f4')),
                ('r_duration', models.CharField(max_length=200, verbose_name='\u9519\u8bef\u6301\u7eed\u65f6\u95f4')),
                ('r_comments', models.CharField(default=b'null', max_length=200, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='monitorItems',
            fields=[
                ('m_ID', models.IntegerField(unique=True, serialize=False, verbose_name='\u63a5\u53e3id', primary_key=True)),
                ('m_class', models.CharField(max_length=200, verbose_name='\u63a5\u53e3\u6240\u5c5e\u7c7b\u522bGroupon,focus,data')),
                ('m_interface', models.CharField(max_length=200, verbose_name='\u63a5\u53e3\u540d\u5b57')),
                ('m_params', models.CharField(max_length=200, verbose_name='\u8bf7\u6c42\u53c2\u6570')),
                ('m_expStr', models.CharField(max_length=200, verbose_name='\u9884\u671f\u8fd4\u56de\u503c')),
                ('m_expDetailStr', models.CharField(max_length=200, verbose_name='\u9884\u671f\u8be6\u7ec6\u8fd4\u56de\u503c')),
                ('m_alertUsers', models.CharField(max_length=200, verbose_name='\u62a5\u8b66\u63a5\u6536\u4eba')),
            ],
        ),
        migrations.RemoveField(
            model_name='alertrecord',
            name='a_lastMsgTimes',
        ),
        migrations.AddField(
            model_name='alertrecord',
            name='a_alertTimes',
            field=models.IntegerField(default=0, verbose_name='\u62a5\u8b66\u6b21\u6570'),
        ),
    ]
