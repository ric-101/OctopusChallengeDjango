# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('word', models.CharField(max_length=1024, unique=True)),
                ('freq', models.IntegerField(default=0)),
            ],
        ),
    ]
