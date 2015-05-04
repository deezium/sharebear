# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0030_auto_20150408_0529'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='spreadmessage',
            unique_together=set([]),
        ),
    ]
