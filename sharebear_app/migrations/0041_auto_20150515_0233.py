# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0040_auto_20150515_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='genre',
            field=models.IntegerField(default=1, max_length=40, choices=[(1, b'Trap'), (2, b'House'), (3, b'Trance'), (4, b'Bass'), (5, b'Hard Dance'), (6, b'Fuck Genres')]),
            preserve_default=True,
        ),
    ]
