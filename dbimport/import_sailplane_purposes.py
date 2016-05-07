#!/usr/bin/env python

import os
import sys
import csv
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'clubmanager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clubmanager.settings")

from manager.models import Purpose, Organisation

reader = csv.DictReader(open('sailplane_purposes.csv'), delimiter = ',')
reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

organisation = Organisation.objects.filter(name='Aeroklub Celje')[0]

for purpose in reader:
   p = Purpose()
   p.type = purpose['type'].strip()
   p.name = unicode(purpose['name'].strip(), 'utf-8')
   p.organisation =  organisation
   
   p.save()
   
   print u'Imported purpose %s -> %s' % (p.type, p.name)
   