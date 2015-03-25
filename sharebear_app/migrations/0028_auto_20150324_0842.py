# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0027_messagelike_liked_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagelike',
            name='liked_at',
            field=models.DateTimeField(default=None, auto_now=True),
            preserve_default=True,
        ),
    ]
