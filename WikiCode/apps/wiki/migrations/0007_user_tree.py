# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-08 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0006_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tree',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
