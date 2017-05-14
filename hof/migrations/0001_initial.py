# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('chinesename', models.CharField(max_length=50)),
                ('preferredname', models.CharField(max_length=50)),
                ('division', models.CharField(max_length=50)),
                ('depart', models.CharField(max_length=50)),
                ('section', models.CharField(max_length=50)),
                ('hc', models.CharField(max_length=50)),
                ('bcnt', models.PositiveIntegerField()),
                ('bscore', models.PositiveIntegerField()),
                ('ccnt', models.PositiveIntegerField()),
                ('cscore', models.PositiveIntegerField()),
                ('icnt', models.PositiveIntegerField()),
                ('iscore', models.PositiveIntegerField()),
                ('qcnt', models.PositiveIntegerField()),
                ('qscore', models.PositiveIntegerField()),
                ('cocnt', models.PositiveIntegerField()),
                ('coscore', models.PositiveIntegerField()),
                ('totalcnt', models.PositiveIntegerField()),
                ('totalscore', models.PositiveIntegerField()),
            ],
        ),
    ]
