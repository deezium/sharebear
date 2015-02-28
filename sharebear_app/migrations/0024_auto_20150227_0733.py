# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharebear_app', '0023_auto_20150223_0241'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_liked', models.BooleanField(default=False, verbose_name=b'Liked')),
                ('ever_liked', models.BooleanField(default=False, verbose_name=b'Ever Liked')),
                ('msg', models.ForeignKey(related_name='message_likes', to='sharebear_app.Message')),
                ('user', models.ForeignKey(related_name='user_likes', verbose_name=b'Liking user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='feedstory',
            name='msg',
        ),
        migrations.RemoveField(
            model_name='feedstory',
            name='user',
        ),
        migrations.DeleteModel(
            name='FeedStory',
        ),
    ]
