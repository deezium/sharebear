# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0026_auto_20150227_0746'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagelike',
            name='liked_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 24, 8, 41, 58, 908282), auto_now=True),
            preserve_default=True,
        ),
    ]
