# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0020_auto_20150127_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='promoter_score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
