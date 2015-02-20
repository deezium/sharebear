# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0021_userprofile_promoter_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='promoter_score_last_updated',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='promoter_score_update_level',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
