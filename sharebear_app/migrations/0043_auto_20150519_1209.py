# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0042_auto_20150515_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackplay',
            name='user',
            field=models.ForeignKey(related_name='user_track_plays', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
