# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertStrategy', '0007_monitorresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitorresult',
            name='m_ID',
        ),
        migrations.DeleteModel(
            name='monitorResult',
        ),
    ]
