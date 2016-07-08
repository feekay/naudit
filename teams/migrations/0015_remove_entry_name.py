# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0014_entry_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='name',
        ),
    ]
