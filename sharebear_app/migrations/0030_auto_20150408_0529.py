# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0029_auto_20150325_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='aboutme',
            field=models.TextField(default=b'I am a trapaholic.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.TextField(default=b'Erf.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='relationship',
            unique_together=set([('from_person', 'to_person', 'status')]),
        ),
    ]
