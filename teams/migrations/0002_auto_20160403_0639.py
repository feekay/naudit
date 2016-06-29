# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='father_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='full_name',
        ),
    ]
