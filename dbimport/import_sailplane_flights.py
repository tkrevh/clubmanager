#!/usr/bin/env python

import os
import sys
import csv
import datetime
import logging

os.environ['DJANGO_SETTINGS_MODULE'] = 'clubmanager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clubmanager.settings")

from manager.models import Aircraft, Purpose, Member, Logbook, Organisation, Flight


logger = logging.getLogger('import_sailplane_flights')
hdlr = logging.FileHandler('import_sailplane_flights.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

reader = csv.DictReader(open('sailplane_flights.csv'), delimiter = ',')
reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

organisation = Organisation.objects.filter(name='Aeroklub Celje')[0]

IMPORT_TYPE = 'sailplane'
counter = 1

for flight in reader:
   print "Importing line #%s: %s" % (counter, flight)
   counter += 1

   try:
      if not flight['datum']:
         print 'Skipping flight, datum empty !'
         logger.warn('Skipping flight, datum empty ! Current data: %s' % (flight))
         continue
         
      flight_date = datetime.datetime.strptime(flight['datum'].strip(), '%Y-%m-%d')
      pilot1 = flight['pilot2'].strip()
      pilot2 = flight['pilot1'].strip()
      letalo = flight['letalo'].strip()
      namen = flight['namen'].strip()
      # prazne namene pretvori v zone
      if not namen:
         namen = 'zona'
      vzlet = flight['vzlet'].strip()
      odpel = flight['odpel'].strip()
      pristal = flight['pristal'].strip()
      km = flight['km'].strip()
      znacka = flight['znacka'].strip()
      vrstaleta = flight['vrstaleta'].strip()
      opombe = flight['opombe'].strip()
      
      if ((pilot1 == '0' or pilot1 == '65535') and (pilot2 == '0' or pilot2 == '65535')):
         print 'Skipping flight on date %s, from %s to %s (%s). Both pilots uknown !' % (flight_date, vzlet, pristal, opombe)
         logger.warn('Skipping flight. Both pilots uknown ! Current data: %s' % (flight))
         continue

      if Member.objects.filter(external_id=pilot1).exists():
         pic = Member.objects.filter(external_id=pilot1)[0]
      else:
         pic = None
         
      if Member.objects.filter(external_id=pilot2).exists():
         instructor = Member.objects.filter(external_id=pilot2)[0]
      else:
         instructor = None
         
      if not pic:
         if not instructor:
            print 'Skipping flight on date %s, from %s to %s (%s). Both pilots uknown !' % (flight_date, vzlet, pristal, opombe)
            logger.warn('Skipping flight. Both pilots uknown ! Current data: %s' % (flight))
            continue
         else:
            pic = instructor
            instructor = None
         
      if not Aircraft.objects.filter(external_id=letalo, type=IMPORT_TYPE).exists():
         print 'Skipping flight on date %s, from %s to %s (%s). Aircraft with external_id=%s does not exist!' % (flight_date, vzlet, pristal, opombe, letalo)
         logger.warn('Skipping flight. Aircraft with external_id=%s does not exist ! Current data: %s' % (letalo, flight))
         continue
      aircraft = Aircraft.objects.filter(external_id=letalo, type=IMPORT_TYPE)[0]
      
      if not Purpose.objects.filter(type=IMPORT_TYPE, name=namen).exists():
         print 'Skipping flight on date %s, from %s to %s (%s). Purpose %s for type %s does not exist!' % (flight_date, vzlet, pristal, opombe, namen, IMPORT_TYPE)
         logger.warn('Skipping flight. Purpose %s for type %s does not exist ! Current data: %s' % (namen, IMPORT_TYPE, flight))
         continue
      purpose = Purpose.objects.filter(type=IMPORT_TYPE, name=namen)[0]

      logbook, created = Logbook.objects.get_or_create(type=IMPORT_TYPE, date=flight_date, organisation=organisation)
      if created:
         logbook.save()

      f = Flight()
      f.date = flight_date
      f.organisation = organisation
      f.pilot = pic
      f.first_name = pic.first_name
      f.last_name = pic.last_name
      if instructor:
         f.instructor = instructor
         f.instructor_first_name = instructor.first_name
         f.instructor_last_name = instructor.last_name
      f.aircraft = aircraft
      f.make = aircraft.make
      f.model = aircraft.model
      f.serial_number = aircraft.serial_number
      f.registration = aircraft.registration
      f.time_takeoff = datetime.datetime.strptime(vzlet, '%H:%M:%S').time()
      if odpel != '00:00:00':
         f.time_release = datetime.datetime.strptime(odpel, '%H:%M:%S').time()
      f.time_landing = datetime.datetime.strptime(pristal, '%H:%M:%S').time()
      f.remark = opombe
      f.logbook = logbook
      f.purpose = purpose
      
      f.save()
      
      print u'Successfully imported flight #%s' % (counter)
      
   except:
      print "Unexpected error:", sys.exc_info()[0]
      print "Error in line: %s" % (flight)
      logger.warn('Fatal error! Current data: %s' % (flight))
      raise
