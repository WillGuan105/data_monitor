# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0013_auto_20160115_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoritems',
            name='m_ID',
        ),
        migrations.AddField(
            model_name='monitoritems',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=datetime.datetime(2016, 2, 3, 2, 27, 40, 699247, tzinfo=utc), serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
