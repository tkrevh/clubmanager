import collections

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.db.models import Q
from manager.models import *


@dajaxice_register(method='GET')
def sayhello(request):
    return simplejson.dumps({'message':'Hello World'})
    
@dajaxice_register(method='GET')
def get_entry(request, search_data, field_id):
      if search_data:
         result = Entry.objects.filter(name__istartswith=search_data) | Entry.objects.filter(content__icontains=search_data)
      else: # search data empty, return all
         result = Entry.objects.all()[:10]
      results = []   
      for entry in result:
         d = collections.OrderedDict()
         d['id'] = entry.pk
         d['value'] = "%s: %s" % (entry.name, entry.content[1:100])
         results.append(d)
      
      return simplejson.dumps({'field_id': field_id, 'results': results})
      
