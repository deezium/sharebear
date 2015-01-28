# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharebear_app', '0018_auto_20150126_0408'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.ForeignKey(related_name='feed_messages', to='sharebear_app.Message')),
                ('user', models.ForeignKey(related_name='feed_stories', verbose_name=b'Recipient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='creator',
        ),
    ]
