""" User models."""
from __future__ import unicode_literals

from django.conf import settings

from django.contrib.auth.hashers import (
    check_password, make_password,
)

from django.core.mail import send_mail
from django.db import models

from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

class BaseUserManager(models.Manager):

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

class EmailUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password,
                                 **extra_fields)
    create = create_user

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password,
                                 **extra_fields)

from common import fields as customFields
from django.db import models as standardFields

@python_2_unicode_compatible
class AbstractBaseUser(models.Model):
    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

class Users(AbstractBaseUser):
    id          = standardFields.AutoField(   _("User UID")  , db_column="user_id"        , primary_key=True)
    password    = standardFields.CharField(   _('Password')  , db_column="password_hash"  , max_length=82)
    email       = standardFields.EmailField(  _('Email')     , db_column="email"          , max_length=128, unique=True, db_index=True)
    name        = standardFields.CharField(   _("Nickname")  , db_column="name"           , max_length=128)
    phone       = standardFields.CharField(   _("Telephone") , db_column="phone"          , max_length=20)
    city        = standardFields.CharField(   _("City")      , db_column="city"           , max_length=50)
    address     = standardFields.CharField(   _("Address")   , db_column="address"        , max_length=255, blank=True)
    is_active   = standardFields.BooleanField(_('Active')    , db_column="active"         , default=True)
    date_joined =   customFields.TimeStamp(   _('Join date '), db_column="createTimestamp")
    points      = models.PositiveIntegerField(_("Points")    , db_column="points"         , default=0)

    is_superuser = is_staff = False

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def givePoints(self, qty):
        self.points += qty
        self.save()
        return self.points

    def setWatching(self, program):
        return self.givePoints(program.points)

    def checkPrizeAvailable(self, prize_points):
        if self.points >= prize_points:
            return True
        return False

    def takePoints(self, pointsRequired):
        if not self.checkPrizeAvailable(pointsRequired):
            raise ValueError("points")
        self.points -= pointsRequired;
        self.save()
        return self.points

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class EVENT_TYPES:
    GET = "GET_POINTS"
    PAY = "PAY_POINTS"

class UserLog(models.Model):
    id = models.AutoField(primary_key=True, db_column="user_log_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="events")
    eventType = models.CharField(max_length=255)
    details   = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    time =   customFields.TimeStamp(db_column="createTimestamp")
    class Meta:
        db_table = "user_log"

