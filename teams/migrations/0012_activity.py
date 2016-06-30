# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=10)),
                ('obj', models.CharField(max_length=10, null=True)),
                ('action', models.CharField(max_length=20)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
