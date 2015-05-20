# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0044_auto_20150519_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artist_name', models.CharField(max_length=40)),
                ('entry_text', models.TextField()),
                ('artist_image', models.FileField(default=b'avatar/user_icon.jpg', upload_to=b'artists')),
                ('song_link1', models.CharField(max_length=200)),
                ('song_link2', models.CharField(max_length=200, null=True, blank=True)),
                ('song_link3', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
