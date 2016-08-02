# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0018_auto_20160713_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='b_owner',
            field=models.ForeignKey(related_name='bowner_set', blank=True, to='teams.Member', null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='c_owner',
            field=models.ForeignKey(related_name='cowner_set', blank=True, to='teams.Member', null=True),
        ),
    ]
