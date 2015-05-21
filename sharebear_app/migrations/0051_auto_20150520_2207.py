# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0050_auto_20150520_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_page',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='soundcloud_page',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
