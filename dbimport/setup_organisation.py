#!/usr/bin/env python

import os
import sys
import csv
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'clubmanager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clubmanager.settings")

from manager.models import Organisation
from django.contrib.auth.models import User

user = User.objects.filter(username='admin')[0]

o = Organisation()
o.name = 'Aeroklub Celje'
o.website = 'www.aeroklub-celje.si'
o.email = 'aeroklub_celje@siol.net'
o.address = 'Medlog 20'
o.city = 'Celje'
o.zip = '3000'
o.country = 'Slovenia'
o.vatid = '12445118'
o.phone1 = '+38635472030'
o.administrator = user
o.save()