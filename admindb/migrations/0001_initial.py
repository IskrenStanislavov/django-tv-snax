# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminFiles',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('table', models.CharField(max_length=255)),
                ('relationId', models.PositiveIntegerField()),
                ('filePath', models.CharField(max_length=255)),
                ('originalFileName', models.CharField(max_length=255)),
                ('fieldName', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('table', 'fieldName', 'relationId'),
                'db_table': '_files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminUsers',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('userName', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '_users',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='adminfiles',
            unique_together=set([('table', 'fieldName', 'relationId')]),
        ),
    ]
