# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0051_auto_20150520_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredentry',
            name='current_followers',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
