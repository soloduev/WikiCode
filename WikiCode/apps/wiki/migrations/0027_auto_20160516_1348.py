# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-16 10:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0026_auto_20160516_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colleague',
            old_name='id_user',
            new_name='user',
        ),
    ]