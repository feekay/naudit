# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20160403_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(max_length=2, choices=[(b'b', b'B'), (b'a', b'A'), (b'c', b'C')]),
        ),
    ]
