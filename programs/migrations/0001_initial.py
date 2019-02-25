# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pr',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'program_id')),
                ('name', models.CharField(max_length=255)),
                ('schedule', common.fields.TimeStampField()),
                ('activeFrom', common.fields.TimeStampField()),
                ('activeTo', common.fields.TimeStampField()),
                ('points', models.PositiveIntegerField()),
                ('description', common.fields.CustomTextField()),
                ('channel', models.CharField(max_length=255)),
                ('createTimestamp', common.fields.TimeStamp()),
                ('audio', common.fields.MediumUnsignedInt8OneToOneField(related_name='programs', null=True, to='recognition.TVSong')),
            ],
            options={
                'ordering': ('name', 'pk'),
                'db_table': 'Programs',
            },
            bases=(models.Model,),
        ),
    ]
