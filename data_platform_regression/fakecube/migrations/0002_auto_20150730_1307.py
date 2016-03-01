# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fakecube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fakecubeif',
            name='f_id',
            field=models.IntegerField(unique=True, verbose_name='Fakecube\u63a5\u53e3id'),
        ),
        migrations.AlterField(
            model_name='fakecubeif',
            name='f_name',
            field=models.CharField(max_length=300, verbose_name='Fakecube\u63a5\u53e3name'),
        ),
        migrations.AlterField(
            model_name='fakecubeif',
            name='frun_url',
            field=models.TextField(verbose_name='\u67e5\u8be2\u63a5\u53e3\u6570\u636e\u7684url'),
        ),
    ]
