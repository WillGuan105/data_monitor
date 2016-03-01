# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpagetest', '0002_checkdiffitems_c_otherparams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkdiffitems',
            name='c_active',
        ),
        migrations.RemoveField(
            model_name='checkdiffitems',
            name='c_host',
        ),
    ]
