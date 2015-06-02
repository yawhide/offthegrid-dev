# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='event starts')),
                ('end_time', models.DateTimeField(verbose_name='event ends')),
                ('location', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('facebook_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('vehicle', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('food', models.CharField(max_length=100)),
                ('img', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='vendors',
            field=models.ManyToManyField(to='vendors.Vendor'),
        ),
    ]
