# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FingerPrint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('audio_id', common.fields.MediumUnsignedInt8()),
                ('offset', common.fields.UnsignedInt10(db_index=True)),
                ('hash', common.fields.Binary10HashField()),
            ],
            options={
                'db_table': 'fingerprints',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TVSong',
            fields=[
                ('audio_id', common.fields.MediumUnsignedInt8Auto(unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('fingerprinted', models.BooleanField(blank=True, default=False, db_column=b'fingerprintStatus')),
                ('hashes', models.IntegerField(default=0, db_column=b'fingerprintHashes')),
                ('timestamp', common.fields.TimeStamp(db_column=b'createTimestamp')),
            ],
            options={
                'db_table': 'audio',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='fingerprint',
            unique_together=set([('audio_id', 'offset', 'hash')]),
        ),
    ]
