#!/usr/bin/env python

import os
import sys
import csv
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'clubmanager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clubmanager.settings")

from manager.models import Aircraft, Organisation

reader = csv.DictReader(open('powered.csv'), delimiter = ',')
reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

organisation = Organisation.objects.filter(name='Aeroklub Celje')[0]

for aircraft in reader:
   a = Aircraft()
   a.type = 'powered'
   a.make = 'Neznan'
   a.model = unicode(aircraft['tip'].strip(), 'utf-8')
   a.serial_number = 'Neznana'
   a.registration = unicode(aircraft['oznaka'].strip(), 'utf-8')
   a.competition_number = unicode(aircraft['kratica'].strip().upper(), 'utf-8')
   a.external_id = aircraft['num'].strip()
   a.ownership = 'club'
   a.organisation = organisation
   
   a.save()
   
   print u'Imported powered aircraft %s %s' % (a.model, a.registration)
   