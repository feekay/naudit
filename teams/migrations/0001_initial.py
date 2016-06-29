# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('key', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('item', models.FileField(upload_to=b'/attachments')),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('due_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('job_id', models.IntegerField()),
                ('address', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField()),
                ('route_date', models.DateField()),
                ('description', models.TextField(max_length=1500)),
                ('approved', models.BooleanField(default=False)),
                ('company', models.ForeignKey(to='teams.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Entry_based',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=50)),
                ('father_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=16)),
                ('gender', models.CharField(max_length=2, choices=[(b'm', b'Male'), (b'f', b'Female')])),
                ('picture', models.ImageField(upload_to=b'profile_pictures')),
                ('cnic', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
                ('birth_date', models.DateField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salary_based',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salary', models.IntegerField()),
                ('details', models.OneToOneField(to='teams.Member')),
            ],
        ),
        migrations.AddField(
            model_name='entry_based',
            name='details',
            field=models.OneToOneField(to='teams.Member'),
        ),
        migrations.AddField(
            model_name='entry_based',
            name='entries',
            field=models.ManyToManyField(to='teams.Entry'),
        ),
        migrations.AddField(
            model_name='entry',
            name='owner',
            field=models.ForeignKey(to='teams.Member'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='entry',
            field=models.ForeignKey(to='teams.Entry'),
        ),
    ]
