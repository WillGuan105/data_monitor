# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fakecube', '0003_fakecubeif_f_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='FakecubeIFResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fresult_id', models.IntegerField(verbose_name='Fakecube\u63a5\u53e3\u7ed3\u679cid')),
                ('f_status', models.CharField(max_length=200, verbose_name='\u8fd0\u884c\u7ed3\u679c\u72b6\u6001')),
                ('f_id', models.ForeignKey(to='fakecube.FakecubeIF')),
            ],
        ),
    ]
