# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0031_auto_20150426_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.TextField(default=b'The greatest place on Earth.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
