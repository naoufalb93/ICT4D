from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from phonenumber_field.modelfields import PhoneNumberField

from . import Language
from . import VoiceService


class KasaDakaUser(models.Model):
    """
    User that belongs to a Voice Service on this system
    """
    caller_id = models.CharField('phone number', max_length=100)
    # phone_number = PhoneNumberField()
    first_name = models.CharField('first name', max_length=100, blank=True)
    last_name = models.CharField('last name', max_length=100, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(VoiceService, on_delete=models.CASCADE)

    def __str__(self):
        if not (self.first_name or self.last_name):
            return "%s" % self.caller_id
        else:
            return "%s %s (%s)" % (self.first_name, self.last_name, self.caller_id)


def lookup_kasadaka_user_by_caller_id(caller_id, service):
    """
    If user with caller_id for current voice_service exists, returns User object.
    If user does not exist or caller_id is None, returns None.
    """
    if caller_id:
        try:
            return KasaDakaUser.objects.get(caller_id=caller_id,
                                            service=service)
        except KasaDakaUser.DoesNotExist:
            return None
    return None
