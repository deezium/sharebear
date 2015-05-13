# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0036_trackplay'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackplay',
            name='platform',
            field=models.CharField(default='youtube', max_length=40),
            preserve_default=False,
        ),
    ]
