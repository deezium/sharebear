# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharebear_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=140, verbose_name=b'Subject')),
                ('body', models.TextField(verbose_name=b'Body')),
                ('sent_at', models.DateTimeField(null=True, verbose_name=b'Sent at', blank=True)),
                ('read_at', models.DateTimeField(null=True, verbose_name=b'Read at', blank=True)),
                ('replied_at', models.DateTimeField(null=True, verbose_name=b'Replied at', blank=True)),
                ('sender_deleted_at', models.DateTimeField(null=True, verbose_name=b'Sender deleted at', blank=True)),
                ('recipient_deleted_at', models.DateTimeField(null=True, verbose_name=b'Recipient deleted at', blank=True)),
                ('parent_msg', models.ForeignKey(related_name=b'next_messages', verbose_name=b'Parent Message', blank=True, to='sharebear_app.Message', null=True)),
                ('recipient', models.ForeignKey(related_name=b'received_messages', verbose_name=b'Recipients', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name=b'sent_messages', verbose_name=b'Sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
    ]
