# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0016_auto_20160713_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='finalize_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
