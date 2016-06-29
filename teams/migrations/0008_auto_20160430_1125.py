# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_auto_20160424_1000'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('company', 'job_id')]),
        ),
    ]
