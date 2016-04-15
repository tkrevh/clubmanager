import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta, date
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Directory model
class Listing(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    date_create = models.DateTimeField(_("Created"), default=datetime.datetime.now)

    def __unicode__(self):
      return u'%s' % self.name

    class Meta:
      verbose_name = _("Listing")
      verbose_name_plural = _("Listings")        
      ordering = ('name',)

class Entry(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    content = models.TextField(_("Content"))
    listings = models.ManyToManyField(Listing)
    date_create = models.DateTimeField(_("Created"), default=datetime.datetime.now)

    def __unicode__(self):
      return u'%s' % self.name

    class Meta:
      verbose_name = _("Entry")
      verbose_name_plural = _("Entries")
      ordering = ('date_create','name',)

