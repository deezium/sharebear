# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharebear_app', '0034_auto_20150505_0816'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialShare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform', models.CharField(max_length=40)),
                ('msg', models.ForeignKey(related_name='message_social_shares', to='sharebear_app.Message')),
                ('user', models.ForeignKey(related_name='user_social_shares', verbose_name=b'Sharing user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
