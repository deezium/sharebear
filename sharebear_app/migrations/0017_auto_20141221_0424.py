# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0016_auto_20141221_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(related_name=b'convo_messages', verbose_name=b'Conversation', blank=True, to='sharebear_app.Conversation', null=True),
        ),
    ]
