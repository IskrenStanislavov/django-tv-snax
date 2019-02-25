# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'prize_id')),
                ('name', models.CharField(max_length=255)),
                ('description', common.fields.CustomTextField()),
                ('activeFrom', common.fields.TimeStampField()),
                ('activeTo', common.fields.TimeStampField()),
                ('points', models.PositiveIntegerField()),
                ('added', common.fields.TimeStamp(db_column=b'createTimestamp')),
            ],
            options={
                'ordering': ('points', 'name', 'pk'),
                'db_table': 'prizes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPrize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prize', models.ForeignKey(related_name='user_prizes', to='prizes.Kind')),
                ('user', models.ForeignKey(related_name='user_prizes', to=settings.AUTH_USER_MODEL)),
                ('takenAt', common.fields.TimeStamp(db_column=b'createTimestamp')),
            ],
            options={
                'ordering': ('user', 'prize'),
                'db_table': 'user_prizes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userprize',
            unique_together=set([('user', 'prize')]),
        ),
    ]
