from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from ..creme_core.models.auth import User
from ..creme_core.common.utils import COUNTRIES, ROLES


class Org(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    user_limit = models.IntegerField(default=5)
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)


class Address(models.Model):
    address_line = models.CharField(
        _("Address"), max_length=255, blank=True, default=""
    )
    street = models.CharField(_("Street"), max_length=55, blank=True, default="")
    city = models.CharField(_("City"), max_length=255, blank=True, default="")
    state = models.CharField(_("State"), max_length=255, blank=True, default="")
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, default=""
    )
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, default="")

    def __str__(self):
        return self.city if self.city else ""

    def get_complete_address(self):
        address = ""
        if self.address_line:
            address += self.address_line
        if self.street:
            if address:
                address += ", " + self.street
            else:
                address += self.street
        if self.city:
            if address:
                address += ", " + self.city
            else:
                address += self.city
        if self.state:
            if address:
                address += ", " + self.state
            else:
                address += self.state
        if self.postcode:
            if address:
                address += ", " + self.postcode
            else:
                address += self.postcode
        if self.country:
            if address:
                address += ", " + self.get_country_display()
            else:
                address += self.get_country_display()
        return address


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='profile')
    org = models.ForeignKey(Org, null=True, on_delete=models.CASCADE, blank=True, related_name="user_org")
    profile_image = models.ImageField(upload_to='avatars', default='avatars/guest.png')
    cover_image = models.ImageField(upload_to='avatars', default='avatars/cover.png')
    phone = PhoneNumberField(max_length=20, blank=True, null=True, unique=True) #phone = models.CharField(max_length=20, blank=True)
    alternate_phone = PhoneNumberField(null=True)
    address = models.ForeignKey(Address, related_name="adress_users", on_delete=models.CASCADE, blank=True, null=True,)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default="USER")
    has_sales_access = models.BooleanField(default=False)
    has_marketing_access = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_organization_admin = models.BooleanField(default=False)
    date_of_joining = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return settings.MEDIA_URL + self._meta.get_field('profile_image').get_default()

    def get_cover_image(self):
        if self.cover_image:
            return self.cover_image.url
        return settings.MEDIA_URL + self._meta.get_field('cover_image').get_default()

    class Meta:
        unique_together = (("user", "org"),)

    @property
    def is_admin(self):
        return self.is_organization_admin


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=kwargs['instance'])

    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

