# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_auto_20160430_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='distance',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='expenses',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
