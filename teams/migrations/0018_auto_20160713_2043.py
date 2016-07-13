# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0017_auto_20160713_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry_based',
            name='entries',
        ),
        migrations.AddField(
            model_name='entry',
            name='b_owner',
            field=models.ForeignKey(related_name='bowner_set', to='teams.Member', null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='c_owner',
            field=models.ForeignKey(related_name='cowner_set', to='teams.Member', null=True),
        ),
    ]
