# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0006_monitoritems_m_interval'),
    ]

    operations = [
        migrations.CreateModel(
            name='monitorResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('m_resultID', models.IntegerField(verbose_name='\u76d1\u63a7\u63a5\u53e3\u7ed3\u679cid')),
                ('m_status', models.CharField(max_length=200, verbose_name='\u8fd0\u884c\u7ed3\u679c\u72b6\u6001')),
                ('m_ID', models.ForeignKey(to='alertStrategy.monitorItems')),
            ],
        ),
    ]
