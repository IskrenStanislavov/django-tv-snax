# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from dejavu.database_sql import SQLDatabase

# http://www.w3schools.com/sql/sql_default.asp
statCommand = """ALTER TABLE %s ALTER %s SET DEFAULT 0""" %(SQLDatabase.SONGS_TABLENAME, SQLDatabase.FIELD_FINGERPRINTED)
hashesCommand = """ALTER TABLE %s ALTER %s SET DEFAULT 0""" %(SQLDatabase.SONGS_TABLENAME, SQLDatabase.FIELD_HASHES_NUMBER)

class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(statCommand, reverse_sql=None,
            state_operations=[
                migrations.AlterField("TVSong", "fingerprinted", models.BooleanField(blank=True, default=0, db_column=b'fingerprintStatus'), preserve_default=True),
            ]
        ),
        migrations.RunSQL(hashesCommand, reverse_sql=None,
        	state_operations=[
        		migrations.AlterField(
                    model_name='tvsong',
                    name='hashes',
                    field=models.IntegerField(default=0, db_column=b'fingerprintHashes'),
                    preserve_default=True,
                ),
        	]
        ),
    ]
# ALTER TABLE Persons
# ALTER City SET DEFAULT 'SANDNES'