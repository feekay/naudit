# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0019_auto_20160802_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='route',
            field=models.ForeignKey(blank=True, to='teams.Route', null=True),
        ),
    ]
