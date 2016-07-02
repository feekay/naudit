# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0013_auto_20160701_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
