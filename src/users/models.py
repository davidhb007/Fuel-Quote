from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import template
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address1 = models.CharField(_("address"), max_length=100)
    address2 = models.CharField(
        _("address cont'd"), max_length=100, blank=True)

    city = models.CharField(_("city"), max_length=100)
    state = USStateField(_("state"))
    zipcode = models.PositiveIntegerField(_("zip code"))

    def __str__(self):
        if not self.address2:
            return self.address1 + ", " + self.city + ", " + self.state + " " + str(self.zipcode)
        else:
            return self.address1 + ", " + self.address2 + ", " + self.city + ", " + self.state + " " + str(self.zipcode)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=50, blank=False, null=False)
    last_name = models.CharField(
        max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}'s Profile"
