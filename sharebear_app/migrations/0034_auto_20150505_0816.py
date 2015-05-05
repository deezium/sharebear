# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0033_auto_20150505_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pic',
            field=models.FileField(default=b'avatars/user_icon.jpg', upload_to=b'avatars'),
            preserve_default=True,
        ),
    ]
