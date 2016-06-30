# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0010_auto_20160525_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('text', models.CharField(max_length=500)),
                ('frm', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('to', models.ManyToManyField(related_name='reciever', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
