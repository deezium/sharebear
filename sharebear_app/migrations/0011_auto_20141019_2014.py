# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0010_auto_20141012_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metamessage',
            name='meta_sub',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pic',
            field=models.FileField(default=b'avatars/finger.jpg', upload_to=b'avatars'),
        ),
    ]
