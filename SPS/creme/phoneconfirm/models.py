from datetime import timedelta

from django.conf import settings
from django.contrib.sites.models import Site
from ..creme_core.models.auth import Account, CremeUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from . import sms
from .managers import PhoneNumberManager, PhoneConfirmationManager
from .utils import digits_only


class PhoneNumber(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=50, unique=True)
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    digits_only = models.CharField(max_length=50, unique=True)
    country_code = models.ForeignKey('PhoneCountryCode', blank=True, null=True, on_delete=models.CASCADE)
    failed_attempts = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        from .utils import digits_only  # Thay 'your_app' bằng tên ứng dụng của bạn
        self.digits_only = digits_only(phone=self.phone_number, country_code=self.country_code)
        super().save(*args, **kwargs)

    objects = PhoneNumberManager()

    def set_as_primary(self, conditional=False):
        old_primary = PhoneNumber.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        return True

    def __unicode__(self):
        return u"%s (%s)" % (self.phone_number, self.user)

    class Meta:
        verbose_name = _("phone number")
        verbose_name_plural = _("phone numbers")


class PhoneCountryCode(models.Model):

    country_name = models.CharField(max_length=255)
    country_short = models.CharField(max_length=2)
    country_code = models.IntegerField()
    starting_number = models.PositiveIntegerField(db_index=True)
    country_regex = models.CharField(max_length=255)
    mobile_number_regex = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.country_name, self.country_code)

    @property
    def mno(self):
        if self.mobilenetworkoperator_set.count():
            return self.mobilenetworkoperator_set.all()[0].mno_value
        return None

    class Meta:
        verbose_name = _("phone country code")
        verbose_name_plural = _("phone country codes")
        ordering = ("country_name",)


class PhoneConfirmation(models.Model):

    phone_country_code = models.ForeignKey('PhoneCountryCode', on_delete=models.CASCADE)
    phone_number = models.ForeignKey('PhoneNumber', on_delete=models.CASCADE)
    sent = models.DateTimeField(editable=False)
    confirm_code = models.CharField(max_length=40)

    objects = PhoneConfirmationManager()

    def code_expired(self):
        expiration_date = self.sent + timedelta(days=settings.PHONE_CONFIRMATION_DAYS)
        return expiration_date <= timezone.now()
    code_expired.boolean = True

    def resend(self):
        sms.send_confirmation(
            user=self.phone_number.user,
            site=Site.objects.get_current(),
            code=self.confirm_code,
            number=self.phone_number.digits_only
        )
        self.sent = timezone.now()
        self.save()

    def __unicode__(self):
        return u"confirmation for %s" % self.phone_number.phone_number

    class Meta:
        verbose_name = _("phone confirmation")
        verbose_name_plural = _("phone confirmations")


class SMSLog(models.Model):
    mocked = models.BooleanField(default=False)
    endpoint = models.CharField(max_length=256)
    payload = models.JSONField()
    number = models.CharField(max_length=50)
    response_code = models.CharField(max_length=16, null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class MessageTooLong(models.Model):

    digits = models.CharField(max_length=100)
    notice_type = models.CharField(max_length=250)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
