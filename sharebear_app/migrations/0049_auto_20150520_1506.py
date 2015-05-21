# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0048_featuredentry_profile_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredentry',
            name='song_link1',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='featuredentry',
            name='song_link2',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='featuredentry',
            name='song_link3',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
