# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20160403_0655'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('route_image', models.FileField(upload_to=b'/routes')),
                ('route_date', models.DateField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='route',
            field=models.ForeignKey(to='teams.Route', null=True),
        ),
    ]
