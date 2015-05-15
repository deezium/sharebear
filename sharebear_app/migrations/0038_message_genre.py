# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0037_trackplay_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='genre',
            field=models.IntegerField(default=1, max_length=40, choices=[(1, b'Trap'), (2, b'House'), (3, b'Trance'), (4, b'Bass'), (5, b'Electro'), (6, b'Hard Dance'), (7, b'Fuck Genres')]),
            preserve_default=True,
        ),
    ]
