# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-01-02 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0051_statistics_total_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='permissions',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
