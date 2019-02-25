# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import common.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='User UID', primary_key=True, db_column='user_id')),
                ('password', models.CharField(max_length=82, verbose_name='Password', db_column='password_hash')),
                ('email', models.EmailField(unique=True, max_length=128, verbose_name='Email', db_column='email', db_index=True)),
                ('name', models.CharField(max_length=128, verbose_name='Nickname', db_column='name')),
                ('phone', models.CharField(max_length=20, verbose_name='Telephone', db_column='phone')),
                ('city', models.CharField(max_length=50, verbose_name='City', db_column='city')),
                ('address', models.CharField(max_length=255, verbose_name='Address', db_column='address', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active', db_column='active')),
                ('date_joined', common.fields.TimeStamp(verbose_name='Join date ', db_column='createTimestamp')),
                ('points', models.PositiveIntegerField(default=0, verbose_name='Points', db_column='points')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
                'db_table': 'users',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='user_log_id')),
                ('eventType', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=255)),
                ('points', models.IntegerField(default=0)),
                ('time', common.fields.TimeStamp(db_column='createTimestamp')),
                ('user', models.ForeignKey(related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_log',
            },
            bases=(models.Model,),
        ),
    ]
