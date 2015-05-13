# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharebear_app', '0035_socialshare'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackPlay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('played_at', models.DateTimeField(default=None, auto_now=True)),
                ('msg', models.ForeignKey(related_name='message_track_plays', to='sharebear_app.Message')),
                ('user', models.ForeignKey(related_name='user_track_plays', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
