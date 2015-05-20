# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0047_auto_20150520_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredentry',
            name='profile_link',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
