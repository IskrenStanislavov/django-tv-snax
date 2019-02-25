from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db import models as standardFields
from common import fields as customFields

from admindb.models import AdminFiles 

class Kind(models.Model):
	# :name, :points, :description, :schedule, :photo, activeFrom , activeTo
    id          = standardFields.AutoField(primary_key=True, db_column="prize_id")
    name    	= standardFields.CharField(max_length=255,blank=False)
    description =   customFields.CustomTextField() # "text"
    activeFrom  =   customFields.TimeStampField()
    activeTo    =   customFields.TimeStampField()
    points      = standardFields.PositiveIntegerField() # 0 to 2147483647
    added       =   customFields.TimeStamp(db_column="createTimestamp")

    def isActive(self):
        now = timezone.now()
        return ( now > self.activeFrom and now < self.activeTo)
    active = property(isActive)

    # def getPrizeedQuantity(self):
    # 	return len(self.user_prizes)
    # prizeed = property(getPrizeedQuantity)

    def boughtByUser(self, user):
        if settings.FILTER_USER_PRIZES_THROUGH_PRIZE: #chose faster one
            querry = self.user_prizes.filter(user_id=user.id)
        else:
            querry = user.user_prizes.filter(prize_id=self.id)
        return querry.exists()

    def getPrizeId(self):
        return self.id
    prizeId = property(getPrizeId)

    def getPhoto(self):
        photo = AdminFiles.objects.get(
            models.Q(table="prizes"),
            models.Q(fieldName='photo'),
            models.Q(relationId=self.id)
        )
        return photo.filePath
    photo = property(getPhoto)

    class Meta:
        db_table = "prizes"
        ordering = ("points", 'name', 'pk')

class UserPrize(models.Model):

    prize   = models.ForeignKey( Kind, related_name="user_prizes" ) # no limit in size
    user 	= models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_prizes" ) # no limit in size
    takenAt =   customFields.TimeStamp(db_column="createTimestamp")

    class Meta:
        db_table = "user_prizes"
        ordering = ('user', 'prize')
        unique_together = ('user', 'prize')

