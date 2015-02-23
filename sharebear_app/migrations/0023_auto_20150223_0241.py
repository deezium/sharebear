# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebear_app', '0022_auto_20150211_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(choices=[(1, b'Following'), (2, b'Blocked')])),
                ('from_person', models.ForeignKey(related_name='from_people', to='sharebear_app.UserProfile')),
                ('to_person', models.ForeignKey(related_name='to_people', to='sharebear_app.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='relationships',
            field=models.ManyToManyField(related_name='related_to', through='sharebear_app.Relationship', to='sharebear_app.UserProfile'),
            preserve_default=True,
        ),
    ]
