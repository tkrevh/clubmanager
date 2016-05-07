import collections

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.db.models import Q
from manager.models import *


@dajaxice_register(method='GET')
def sayhello(request):
    return simplejson.dumps({'message':'Hello World'})
    
@dajaxice_register(method='GET')
def get_pilot(request, search_data, field_id):
      if search_data:
         search_data = search_data.replace('*','.')
         split_search = search_data.split('.')
         split_search_len = len(split_search)
         p_last_name = split_search[0]
         p_first_name = ''
         if split_search_len > 1:
            p_last_name = split_search[1]
            p_first_name = split_search[0]
         if p_first_name:
            result = Member.objects.filter(organisation__administrator=request.user).filter(first_name__istartswith=p_first_name).filter(last_name__istartswith=p_last_name)
         else:
            result = Member.objects.filter(organisation__administrator=request.user).filter(last_name__istartswith=p_last_name)
      else: # search data empty, return all
         result = Member.objects.filter(organisation__administrator=request.user)
      results = []   
      for pilot in result:
         d = collections.OrderedDict()
         d['id'] = pilot.pk
         d['value'] = pilot.first_name + ' ' +pilot.last_name
         results.append(d)
      
      return simplejson.dumps({'field_id': field_id, 'results': results})
      
@dajaxice_register(method='GET')
def get_aircraft(request, search_data, type, field_id):
      aircraft_type = type
      if search_data:
         result = Aircraft.objects.filter(organisation__administrator=request.user).filter(type=aircraft_type).filter(Q(make__istartswith=search_data) | Q(model__istartswith=search_data) | Q(registration__startswith=search_data) | Q(competition_number__startswith=search_data))
      else:
         result = Aircraft.objects.filter(organisation__administrator=request.user).filter(type=aircraft_type)
      results = []   
      for aircraft in result:
         d = collections.OrderedDict()
         d['id'] = aircraft.pk
         d['value'] = aircraft.model + ' ' + aircraft.registration
         results.append(d)
      
      return simplejson.dumps({'field_id': field_id, 'results': results})
      
@dajaxice_register(method='GET')
def get_purpose(request, search_data, type, field_id):
      purpose_type = type
      if search_data:
         result = Purpose.objects.filter(organisation__administrator=request.user).filter(type=purpose_type).filter(name__istartswith=search_data)
      else:
         result = Purpose.objects.filter(organisation__administrator=request.user).filter(type=Purpose)
      results = []   
      for purpose in result:
         d = collections.OrderedDict()
         d['id'] = purpose.pk
         d['value'] = purpose.name
         results.append(d)
      return simplejson.dumps({'field_id': field_id, 'results': results})
      
      
@dajaxice_register(method='GET')
def set_flight_event_time(request, flight_id, event_name, time):
      flight = Flight.objects.filter(pk=flight_id)[0]
      setattr(flight, event_name, time);
      flight.save()
      return simplejson.dumps({'flight_id': flight_id, 'event_name': event_name, 'time': time})
      