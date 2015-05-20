# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0045_featuredentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredentry',
            name='post_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'Posted at', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='featuredentry',
            name='artist_image',
            field=models.FileField(default=b'avatar/user_icon.jpg', upload_to=b'avatars'),
            preserve_default=True,
        ),
    ]
