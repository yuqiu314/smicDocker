# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hof', '0002_visitcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('head_image', models.FileField(upload_to=b'images')),
                ('employee', models.ForeignKey(to='hof.Employee')),
            ],
        ),
    ]
