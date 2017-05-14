# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hof.models


class Migration(migrations.Migration):

    dependencies = [
        ('hof', '0007_auto_20160112_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('content_type', models.CharField(max_length=20)),
                ('content_file', models.FileField(max_length=255, upload_to=hof.models.process_content_file, blank=True)),
            ],
        ),
    ]
