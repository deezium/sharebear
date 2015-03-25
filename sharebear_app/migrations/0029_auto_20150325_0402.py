# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0028_auto_20150324_0842'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='spreadmessage',
            unique_together=set([('user', 'msg')]),
        ),
    ]
