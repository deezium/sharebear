# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0007_auto_20141002_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='metamessage',
            name='meta_sub',
            field=models.CharField(default='Sup', max_length=140, verbose_name=b'Meta Subject'),
            preserve_default=False,
        ),
    ]
