# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hof', '0003_employeeimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=255, upload_to=b'excel', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadPPT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=255, upload_to=b'ppt', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='employeeimage',
            name='employee',
        ),
        migrations.AddField(
            model_name='employee',
            name='head_image',
            field=models.FileField(max_length=255, upload_to=b'images', blank=True),
        ),
        migrations.DeleteModel(
            name='EmployeeImage',
        ),
    ]
