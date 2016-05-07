#!/usr/bin/env python

import os
import sys
import csv
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'clubmanager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clubmanager.settings")

from manager.models import Member, Organisation, Document

reader = csv.DictReader(open('members.csv'), delimiter = ',')
reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

organisation = Organisation.objects.filter(name='Aeroklub Celje')[0]


#print fields
for member in reader:
   m = Member()
   m.first_name = member['ime'].strip()
   m.last_name = member['priimek'].strip()
   m.email = member['email'].strip()
   m.address = member['ulica'].strip()
   m.city = member['mesto'].strip()
   m.zip = member['posta'].strip()
   m.country = 'Slovenia'
   m.phone_mobile = member['telefonmobilni'].strip()
   m.phone_home = member['telefondoma'].strip()
   m.phone_work = member['telefonsluzba'].strip()
   m.external_id = member['num'].strip()
   m.organisation = organisation
   
   # correct missing names or last names
   if not m.first_name:
      m.first_name = m.last_name
   if not m.last_name:
      m.last_name = m.first_name
   
   m.save()
   
   if (member['jadralnodovoljenje'] and member['jadralnodovoljenje'].strip() and member['jadralnodovoljenje'].strip() != '0000-00-00'):
      document = Document()
      document.type = 'gpl'
      document.date_of_issue = datetime.datetime.strptime(member['jadralnodovoljenje'].strip(), '%Y-%m-%d')
      document.member = m
      document.save()
      
   if (member['motornodovoljenje'] and member['motornodovoljenje'].strip() and member['motornodovoljenje'].strip() != '0000-00-00'):
      document = Document()
      document.type = 'ppl'
      document.date_of_issue = datetime.datetime.strptime(member['motornodovoljenje'].strip(), '%Y-%m-%d')
      document.member = m
      document.save()
      
   if (member['zdravniskospricevaloveljavnost'] and member['zdravniskospricevaloveljavnost'].strip() and member['zdravniskospricevaloveljavnost'].strip() != '0000-00-00'):
      document = Document()
      document.type = 'medical'
      document.date_of_issue = datetime.datetime.strptime(member['zdravniskospricevaloveljavnost'].strip(), '%Y-%m-%d')
      if (member['zdravniskospricevalorazred'] and member['zdravniskospricevalorazred'].strip() and member['zdravniskospricevalorazred'].strip() != '0'):
         document.document_class = member['zdravniskospricevalorazred'].strip()
      document.member = m
      document.save()
      
   print 'Imported %s, %s, %s  (%s)' % (m.first_name, m.last_name, m.city, m.external_id)
   