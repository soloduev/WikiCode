# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-01-04 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0056_statistics_total_dynamic_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='saves',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='stars',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]