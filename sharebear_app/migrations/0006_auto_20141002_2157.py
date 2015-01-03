# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0005_auto_20141002_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='meta_msg',
            field=models.ForeignKey(related_name=b'sub_messages', default=1, to='sharebear_app.MetaMessage'),
        ),
    ]
