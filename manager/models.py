import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta, date
from django.contrib.auth.models import User
from django.db.models.signals import post_save


AIRCRAFT_TYPE =(
('sailplane', _('Sailplane')),
('powered', _('Powered Aircraft')),
)

BILLING_TYPE =(
('noncommercial', _('Non-commerical')),
('commercial', _('Commercial')),
)

DOCUMENT_TYPE =(
('medical', _('Medical')),
('gpl', _('Glider pilot license')),
('ppl', _('Private pilot license')),
)

OWNERSHIP_TYPE =(
('private', _('Private ownership')),
('club', _('Club ownership')),
)

GENDER =(
('m', _('Male')),
('f', _('Female')),
)

# ClubManager model

class Organisation(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    website = models.CharField(_("Website"), max_length=128, blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=128, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=128)
    city = models.CharField(_("City"), max_length=128)
    zip = models.CharField(_("ZIP"), max_length=16)
    country = models.CharField(_("Country"), max_length=64)
    vatid = models.CharField(_("VAT ID"), max_length=32)
    phone1 = models.CharField(_("Phone 1"), max_length=64)
    phone2 = models.CharField(_("Phone 2"), max_length=64, blank=True, null=True)
    fax = models.CharField(_("Fax"), max_length=64, blank=True, null=True)
    administrator = models.OneToOneField(User)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _("Organisation")
        verbose_name_plural = _("Organisations")

class Member(models.Model):
   user = models.OneToOneField(User, null=True) 
   first_name = models.CharField(_("First name"), max_length=64)
   last_name = models.CharField(_("Last name"), max_length=64)
   email = models.CharField(_("Email"), max_length=64, blank=True, null=True)
   birthday = models.DateField(_("Birthday"), blank=True, null=True)
   gender = models.CharField(_("Gender"), max_length=1, choices = GENDER, blank=True, null=True)
   address = models.CharField(_("Address"), max_length=128, blank=True, null=True)
   city = models.CharField(_("City"), max_length=128, blank=True, null=True)
   zip = models.CharField(_("ZIP"), max_length=16, blank=True, null=True)
   country = models.CharField(_("Country"), max_length=64, blank=True, null=True)
   vatid = models.CharField(_("VAT ID"), max_length=32, blank=True, null=True)
   phone_mobile = models.CharField(_("Mobile Phone"), max_length=64, blank=True, null=True)
   phone_home = models.CharField(_("Home Phone"), max_length=64, blank=True, null=True)
   phone_work = models.CharField(_("Work Phone"), max_length=64, blank=True, null=True)
   fax = models.CharField(_("Fax"), max_length=64, blank=True, null=True)
   organisation = models.ForeignKey(Organisation)
   picture = models.ImageField(_("Picture"), upload_to="member_images/", blank=True, null=True)
   external_id = models.CharField(_("External Id"), max_length=16, blank=True, null=True)

   date_joined = models.DateTimeField(_("Date joined"), default=datetime.datetime.now)
   last_login = models.DateTimeField(_("Last login"), default=datetime.datetime.now)
   last_password_check = models.DateTimeField(_("Last password check"), default=datetime.datetime.now)

   def __unicode__(self):
      return u'%s %s, %s' % (self.first_name, self.last_name, self.city)

   class Meta:
      verbose_name = _("Member")
      verbose_name_plural = _("Members")        

class Document(models.Model):
   type = models.CharField(_("Type"), max_length=20, choices = DOCUMENT_TYPE)
   number = models.CharField(_("Document Number"), max_length=64, blank=True, null=True)
   date_of_issue = models.DateField(_("Date of issue"), blank=True, null=True)
   valid_until = models.DateField(_("Valid until"), blank=True, null=True)
   document_class = models.CharField(_("Class"), max_length=32, blank=True, null=True)
   remark = models.CharField(_("Remark"), max_length=256, blank=True, null=True)
   member = models.ForeignKey(Member)       
      
   def __unicode__(self):
      return u'%s %s %s %s %s' % (self.member.last_name, self.member.first_name, self.type, self.valid_until, self.remark)
    
   class Meta:
     verbose_name = _("Document")
     verbose_name_plural = _("Documents")
     
class Aircraft(models.Model):
   type = models.CharField(_("Type"), max_length=20, choices = AIRCRAFT_TYPE)
   ownership = models.CharField(_("Ownership"), max_length=20, choices = OWNERSHIP_TYPE)
   make = models.CharField(_("Make"), max_length=64)
   model = models.CharField(_("Model"), max_length=64)
   serial_number = models.CharField(_("Serial number"), max_length=64)
   registration = models.CharField(_("Registration"), max_length=16)
   competition_number = models.CharField(_("Competition number"), max_length=4, blank=True, null=True)
   external_id = models.CharField(_("External Id"), max_length=16, blank=True, null=True)
   organisation = models.ForeignKey(Organisation)       
      
   def __unicode__(self):
      return u'%s, %s (%s)' % (self.model, self.registration, self.competition_number)
    
   class Meta:
     verbose_name = _("Airplane")
     verbose_name_plural = _("Airplanes")
     
class Purpose(models.Model):
   type = models.CharField(_("Type"), max_length=20, choices = AIRCRAFT_TYPE)
   name = models.CharField(_("Name"), max_length=64)
   billing_type = models.CharField(_("Billing type"), max_length=20, choices = BILLING_TYPE)
   organisation = models.ForeignKey(Organisation)       
      
   def __unicode__(self):
      return u'%s' % (self.name)
    
   class Meta:
     verbose_name = _("Purpose")
     verbose_name_plural = _("Purposes")
     
   
class Logbook(models.Model):
   type = models.CharField(_("Type"), max_length=20, choices = AIRCRAFT_TYPE)
   date = models.DateField(_("Date"), blank=True, null=True)
   organisation = models.ForeignKey(Organisation)       
      
   def __unicode__(self):
      return u'%s | %s, %s' % (self.date, self.type, self.organisation.name)
    
   class Meta:
     verbose_name = _("Logbook")
     verbose_name_plural = _("Logbooks")
     unique_together = ('type', 'date',)     
   
class Flight(models.Model):
   date = models.DateField(_("Date"), default=datetime.date.today)
   organisation = models.ForeignKey(Organisation)
   pilot = models.ForeignKey(Member, related_name='pilot_flights')
   instructor = models.ForeignKey(Member, blank=True, null=True, related_name='instructor_flights')
   aircraft = models.ForeignKey(Aircraft)
   purpose = models.ForeignKey(Purpose)
   first_name = models.CharField(_("First name"), max_length=128, blank=True, null=True)
   last_name = models.CharField(_("Last name"), max_length=128, blank=True, null=True)
   instructor_first_name = models.CharField(_("Instructor first name"), max_length=128, blank=True, null=True)
   instructor_last_name = models.CharField(_("Instructor last name"), max_length=128, blank=True, null=True)
   make = models.CharField(_("Make"), max_length=64, blank=True, null=True)
   model = models.CharField(_("Model"), max_length=64, blank=True, null=True)
   serial_number = models.CharField(_("Serial number"), max_length=64, blank=True, null=True)
   registration = models.CharField(_("Registration"), max_length=16, blank=True, null=True)
   time_block_off = models.TimeField(_("Block off"), blank=True, null=True)
   time_takeoff = models.TimeField(_("Takeoff"), blank=True, null=True)
   time_tow_release = models.TimeField(_("Tow release"), blank=True, null=True)
   time_landing = models.TimeField(_("Landing"), blank=True, null=True)
   time_block_on = models.TimeField(_("Block off"), blank=True, null=True)
   flight_time = models.TimeField(_("Flight time"), blank=True, null=True)
   remark = models.CharField(_("Remark"), max_length=1024, blank=True, null=True)
   igc_file = models.FileField(_("IGC file"), upload_to="igc/", blank=True, null=True)
   logbook = models.ForeignKey(Logbook)
   
   def __unicode__(self):
      return u'%s %s %s %s %s %s %s' % (self.date, self.organisation.name, self.first_name, self.last_name, self.make, self.model, self.registration)
      
   def total_airborne_time(self):
      if not self.time_takeoff:
         return '0:0';
      if not self.time_landing:
         return '0:0';
         
      delta_time = self.time_landing - self.time_takeoff
      
      print delta_time
      
      hours = delta_time.seconds / 60 / 60 
      minutes = delta_time.seconds / 60
      return '%s:%s' % (hours, minutes)
      
   def __init__(self, *args, **kwargs):
      super(Flight, self).__init__(*args, **kwargs)
      if self.time_landing and self.time_takeoff:
         self.flight_time = (datetime.datetime.min + (datetime.datetime.combine(date.today(), self.time_landing) - datetime.datetime.combine(date.today(), self.time_takeoff))).time()

   def save(self, *args, **kwargs):
      if self.time_landing and self.time_takeoff:
         self.flight_time = (datetime.datetime.min + (datetime.datetime.combine(date.today(), self.time_landing) - datetime.datetime.combine(date.today(), self.time_takeoff))).time()
      if self.logbook:
         self.date = self.logbook.date
      super(Flight, self).save(*args, **kwargs)      
    
   class Meta:
     verbose_name = _("Flight")
     verbose_name_plural = _("Flights")
   