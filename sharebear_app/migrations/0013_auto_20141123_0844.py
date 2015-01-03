# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0012_auto_20141019_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='tagline',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='aboutme',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
