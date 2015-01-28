# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0017_auto_20141221_0424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-creation_time'], 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='sent_at',
            new_name='creation_time',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='sender',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='conversation',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.RemoveField(
            model_name='message',
            name='is_liked',
        ),
        migrations.RemoveField(
            model_name='message',
            name='meta_msg',
        ),
        migrations.DeleteModel(
            name='MetaMessage',
        ),
        migrations.RemoveField(
            model_name='message',
            name='parent_msg',
        ),
        migrations.RemoveField(
            model_name='message',
            name='read_at',
        ),
        migrations.RemoveField(
            model_name='message',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='message',
            name='recipient_deleted_at',
        ),
        migrations.RemoveField(
            model_name='message',
            name='replied_at',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender_deleted_at',
        ),
        migrations.RemoveField(
            model_name='message',
            name='subject',
        ),
    ]
