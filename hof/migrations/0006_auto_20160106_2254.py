# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hof.models


class Migration(migrations.Migration):

    dependencies = [
        ('hof', '0005_auto_20160106_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='showcnt',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='showgrade',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='showrank',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='showscore',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='head_image',
            field=models.FileField(max_length=255, upload_to=hof.models.content_file_name, blank=True),
        ),
    ]
