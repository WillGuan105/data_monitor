# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0003_auto_20151020_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertrecord',
            name='a_InterfaceName',
        ),
        migrations.RemoveField(
            model_name='monitoritems',
            name='m_interface',
        ),
        migrations.AddField(
            model_name='alertrecord',
            name='a_city',
            field=models.CharField(default=datetime.datetime(2015, 10, 21, 8, 34, 34, 867280, tzinfo=utc), max_length=200, verbose_name='\u57ce\u5e02\u5317\u4eac,\u5e7f\u5dde'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alertrecord',
            name='a_class',
            field=models.CharField(default='null', max_length=200, verbose_name='\u63a5\u53e3\u6240\u5c5e\u7c7b\u522bGroupon,focus,data'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alertrecord',
            name='a_errorType',
            field=models.CharField(default='null', max_length=200, verbose_name='\u9519\u8bef\u7c7b\u578b'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alertrecord',
            name='a_name',
            field=models.CharField(default='null', max_length=200, verbose_name='\u540d\u5b57'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alertrecord',
            name='a_plat',
            field=models.CharField(default='null', max_length=200, verbose_name='\u5e73\u53f0pc,mob'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alertreport',
            name='r_alertTimes',
            field=models.IntegerField(default=0, verbose_name='\u62a5\u8b66\u6b21\u6570'),
        ),
        migrations.AddField(
            model_name='alertreport',
            name='r_traceUsers',
            field=models.CharField(default='null', max_length=200, verbose_name='\u95ee\u9898\u8ddf\u8e2a\u4eba'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitoritems',
            name='m_city',
            field=models.CharField(default='null', max_length=200, verbose_name='\u57ce\u5e02\u5317\u4eac,\u5e7f\u5dde'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitoritems',
            name='m_host',
            field=models.CharField(default='null', max_length=200, verbose_name='host -H "host:"'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitoritems',
            name='m_name',
            field=models.CharField(default='null', max_length=200, verbose_name='\u540d\u5b57'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitoritems',
            name='m_plat',
            field=models.CharField(default='null', max_length=200, verbose_name='\u5e73\u53f0pc,mob'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitoritems',
            name='m_url',
            field=models.CharField(default='null', max_length=200, verbose_name='\u8bf7\u6c42url http://'),
            preserve_default=False,
        ),
    ]
