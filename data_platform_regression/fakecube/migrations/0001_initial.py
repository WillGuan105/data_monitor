# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FakecubeIF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f_id', models.IntegerField(unique=True, verbose_name='Fakecubeid')),
                ('f_name', models.CharField(max_length=300, verbose_name='Fakecubename')),
                ('frun_url', models.TextField(verbose_name='url')),
            ],
        ),
    ]
