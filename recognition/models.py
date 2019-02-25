from django.db import models

from common import fields as customFields
from django.db import models as standardFields

class TVSong(models.Model):
    audio_id        =   customFields.MediumUnsignedInt8Auto(    primary_key=True, unique=True )
    name            = standardFields.CharField(                 max_length=255)
    # fingerprinted   =   customFields.TinyIntegerField(          db_column="fingerprintStatus", default=0 )# tinyint
    fingerprinted   = standardFields.BooleanField(              db_column="fingerprintStatus", default=False)
    hashes          = standardFields.IntegerField(              db_column="fingerprintHashes", default=0 )
    timestamp       =   customFields.TimeStamp(                 db_column="createTimestamp")
    # programs        = standardFields.ForeignKey('programs.Pr', null=True, related_name="audio")

    class Meta:
        db_table = "audio"

class FingerPrint(models.Model):
    audio_id    = customFields.MediumUnsignedInt8()
    offset      = customFields.UnsignedInt10(db_index=True)
    hash        = customFields.Binary10HashField()

    class Meta:
        unique_together = ("audio_id", "offset", "hash")
        db_table = "fingerprints"
