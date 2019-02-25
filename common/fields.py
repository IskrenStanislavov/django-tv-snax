
from django.db import models
from django.utils import timezone
from django.conf import settings

# http://stackoverflow.com/questions/11332107/timestamp-fields-in-django
class TimeStamp(models.DateTimeField):
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        else:
            return super(TimeStamp, self).db_type()
    def get_internal_type(self):
        return "TimeStamp"

class TimeStampField(models.DateTimeField):
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "TIMESTAMP NOT NULL DEFAULT 0"
        else:
            return super(TimeStampField, self).db_type()
    def get_internal_type(self):
        return "TimeStampField"

class CustomTextField(models.TextField):
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "text"
        else:
            return super(CustomTextField, self).db_type()
    def get_internal_type(self):
        return "CustomTextField"


# http://stackoverflow.com/questions/11642268/adding-simple-custom-field-to-django-how-to-write-south-introspection-rules
# https://code.djangoproject.com/attachment/ticket/18201/custommodels.py

class UnsignedInt10(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "int(10) unsigned"
        else:
            return super(UnsignedInt10, self).db_type()
    def get_internal_type(self):
        return "UnsignedInt10"

class MediumUnsignedInt8Auto(models.AutoField):       
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "mediumint(8) unsigned AUTO_INCREMENT"
        else:
            return super(MediumUnsignedInt8Auto, self).db_type()
    def get_internal_type(self):
        return "MediumUnsignedInt8"

class MediumUnsignedInt8(models.IntegerField):       
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "mediumint(8) unsigned"
        else:
            return super(MediumUnsignedInt8, self).db_type()
    def get_internal_type(self):
        return "MediumUnsignedInt8"

class MediumUnsignedInt8OneToOneField(models.OneToOneField):       
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "mediumint(8) unsigned"
        else:
            return super(MediumUnsignedInt8, self).db_type()
    def get_internal_type(self):
        return "MediumUnsignedInt8OneToOneField"

class Binary10HashField(models.BinaryField):       
    def db_type(self, connection):
        if settings.DB_ENGINE == 'django.db.backends.mysql':
            return "binary(10) not null"
        else:
            return super(Binary10HashField, self).db_type()
    def get_internal_type(self):
        return "Binary10HashField"

