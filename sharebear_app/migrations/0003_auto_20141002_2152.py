# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0002_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='meta_msg',
            field=models.ForeignKey(related_name=b'sub_messages', default=None, to='sharebear_app.MetaMessage'),
            preserve_default=True,
        ),
    ]
