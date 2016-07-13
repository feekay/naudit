# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0015_remove_entry_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='teamb_desc',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='teamc_desc',
        ),
        migrations.AddField(
            model_name='attachment',
            name='comment',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
