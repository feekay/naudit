# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20160403_0705'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='cleared',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entry',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entry',
            name='finalize_date',
            field=models.DateField(default=datetime.datetime(2016, 4, 24, 9, 59, 55, 586242, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entry',
            name='visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='item',
            field=models.FileField(upload_to=b'attachments'),
        ),
        migrations.AlterField(
            model_name='route',
            name='route_image',
            field=models.FileField(upload_to=b'routes'),
        ),
    ]
