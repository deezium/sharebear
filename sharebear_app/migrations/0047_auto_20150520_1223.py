# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0046_auto_20150520_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredentry',
            name='artist_image',
            field=models.FileField(default=b'avatars/user_icon.jpg', upload_to=b'avatars'),
            preserve_default=True,
        ),
    ]
