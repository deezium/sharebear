# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0014_userprofile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_liked',
            field=models.BooleanField(default=False, verbose_name=b'Liked'),
            preserve_default=True,
        ),
    ]
