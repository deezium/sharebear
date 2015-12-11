# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0053_campaignrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagelike',
            name='liked_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='trackplay',
            name='played_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
