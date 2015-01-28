# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0019_auto_20150127_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedstory',
            name='ever_liked',
            field=models.BooleanField(default=False, verbose_name=b'Ever Liked'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedstory',
            name='is_liked',
            field=models.BooleanField(default=False, verbose_name=b'Liked'),
            preserve_default=True,
        ),
    ]
