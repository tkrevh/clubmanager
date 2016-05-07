#!/usr/bin/env python

import os
import sys
import csv
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'clubmanager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clubmanager.settings")

from manager.models import Aircraft, Purpose, Member, Logbook, Organisation, Flight

reader = csv.DictReader(open('powered_flights.csv'), delimiter = ',')
reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

organisation = Organisation.objects.filter(name='Aeroklub Celje')[0]

# delete all flights and logbooks
Flight.objects.filter(organisation=organisation).delete()
Logbook.objects.filter(organisation=organisation, type='sailplane').delete()
Logbook.objects.filter(organisation=organisation, type='powered').delete()
