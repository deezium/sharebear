# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0006_auto_20141002_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='meta_msg',
            field=models.ForeignKey(related_name=b'sub_messages', to='sharebear_app.MetaMessage'),
        ),
    ]
