# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='teamb_desc',
            field=models.TextField(max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='teamc_desc',
            field=models.TextField(max_length=1500, null=True),
        ),
    ]
