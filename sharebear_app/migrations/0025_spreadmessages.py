# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharebear_app', '0024_auto_20150227_0733'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpreadMessages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.ForeignKey(related_name='message_spreadmessages', to='sharebear_app.Message')),
                ('user', models.ForeignKey(related_name='user_spreadmessages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
