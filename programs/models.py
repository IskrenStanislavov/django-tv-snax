from django.db import models
from django.utils import timezone

from django.db import models as standardFields
from common import fields as customFields

from admindb.models import AdminFiles 

class Pr(models.Model):
    id              = standardFields.AutoField(primary_key=True, db_column="program_id")
    audio           =   customFields.MediumUnsignedInt8OneToOneField('recognition.TVSong', related_name="programs",null=True)
    name            = standardFields.CharField( max_length=255 ) # no limit in size
    schedule        =   customFields.TimeStampField()
    activeFrom      =   customFields.TimeStampField()
    activeTo        =   customFields.TimeStampField()
    points          = standardFields.PositiveIntegerField() # 0 to 2147483647
    description     =   customFields.CustomTextField() # "text"
    channel         = standardFields.CharField( max_length=255 )
    createTimestamp =   customFields.TimeStamp()

    def isActive(self):
        now = timezone.now()
        return ( now > self.activeFrom and now < self.activeTo)
    active = property(isActive)

    def getProgramId(self):
        return self.id
    programId = property(getProgramId)

    def getPhoto(self):
        photo = AdminFiles.objects.get(
            models.Q(table="programs"),
            models.Q(fieldName='photo'),
            models.Q(relationId=self.id)
        )
        return photo.filePath
    photo = property(getPhoto)

    class Meta:
        db_table = "Programs"
        ordering = ('name', 'pk')
