# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('i_ID', models.IntegerField(serialize=False, primary_key=True)),
                ('i_name', models.CharField(max_length=200, verbose_name='\u63a5\u53e3\u540d\u5b57')),
                ('i_params', models.CharField(max_length=200, verbose_name='\u8bf7\u6c42\u53c2\u6570')),
                ('i_status', models.CharField(max_length=200, verbose_name='\u7ed3\u679c\u72b6\u6001')),
            ],
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('m_id', models.IntegerField(serialize=False, primary_key=True)),
                ('m_name', models.CharField(max_length=100, verbose_name='\u6a21\u5757\u540d\u5b57')),
            ],
        ),
        migrations.CreateModel(
            name='runResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('his_id', models.IntegerField(verbose_name='\u62a5\u8868\u7ed3\u679cid')),
                ('status', models.CharField(max_length=200, verbose_name='\u8fd0\u884c\u7ed3\u679c\u72b6\u6001')),
                ('error_request', models.CharField(max_length=500, verbose_name='\u62a5\u9519\u7684\u8bf7\u6c42')),
                ('intf', models.ForeignKey(to='smokeTest.Interface')),
            ],
        ),
        migrations.AddField(
            model_name='interface',
            name='i_module',
            field=models.ForeignKey(to='smokeTest.Modules'),
        ),
    ]
