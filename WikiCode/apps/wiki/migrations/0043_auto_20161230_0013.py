# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-29 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0042_auto_20161107_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='is_contents',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_dynamic_paragraphs',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_file_tree',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_files',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_general_comments',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_links',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_loading',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_protected_edit',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_public',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_saving',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_show_author',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_starring',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='is_versions',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
