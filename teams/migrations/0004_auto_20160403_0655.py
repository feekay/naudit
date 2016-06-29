# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20160403_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_type',
            field=models.CharField(default='a', max_length=2, choices=[(b'b', b'B'), (b'a', b'A'), (b'c', b'C')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(max_length=2, choices=[(b'm', b'Male'), (b'f', b'Female')]),
        ),
    ]
