from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from models import *
from django.core.urlresolvers import reverse
 
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
        
class AircraftMixin(LoginRequiredMixin):
    model = Aircraft
    def get_success_url(self):
        return reverse('aircraft_list')
    def get_queryset(self):
        return Aircraft.objects.filter(organisation__administrator=self.request.user)
        
class MemberMixin(LoginRequiredMixin):
    model = Member
    def get_success_url(self):
        return reverse('member_list')
    def get_queryset(self):
        return Member.objects.filter(organisation__administrator=self.request.user)
        
class DocumentMixin(LoginRequiredMixin):
    model = Document
    def get_success_url(self):
        return reverse('member_update', kwargs={'pk': self.kwargs['member_id']})
    def get_queryset(self):
        member_id=self.kwargs['member_id']
        return Document.objects.filter(member__pk=member_id)
        
class OrganisationMixin(LoginRequiredMixin):
    model = Organisation
    def get_success_url(self):
        return reverse('manager.views.main_menu')
    def get_queryset(self):
        return Organisation.objects.filter(administrator=self.request.user)
        
class LogbookMixin(LoginRequiredMixin):
    model = Logbook
    def get_success_url(self):
        return reverse('logbook_list', kwargs={'type': self.kwargs['type']})
    def get_queryset(self):
        logbook_type=self.kwargs['type']
        return Logbook.objects.filter(organisation__administrator=self.request.user).filter(type=logbook_type).order_by('-date') 

class FlightMixin(LoginRequiredMixin):
    model = Flight
    def get_success_url(self):
        return reverse('logbook_manage', kwargs={'type': self.kwargs['type'], 'logbook_id': self.kwargs['logbook_id']})
    def get_queryset(self):
        logbook_type=self.kwargs['type']
        logbook_id=self.kwargs['logbook_id']
        result = Flight.objects.filter(logbook__organisation__administrator=self.request.user).filter(logbook__type=logbook_type).filter(logbook__pk=logbook_id)
        return result
        
class FlightMixinAdvanced(LoginRequiredMixin):
    model = Flight
    def get_success_url(self):
        return reverse('logbook_manage_advanced', kwargs={'type': self.kwargs['type'], 'logbook_id': self.kwargs['logbook_id']})
    def get_queryset(self):
        logbook_type=self.kwargs['type']
        logbook_id=self.kwargs['logbook_id']
        result = Flight.objects.filter(logbook__organisation__administrator=self.request.user).filter(logbook__type=logbook_type).filter(logbook__pk=logbook_id)
        return result
        
class PurposeMixin(LoginRequiredMixin):
    model = Purpose
    def get_success_url(self):
        return reverse('purpose_list')
    def get_queryset(self):
        return Purpose.objects.filter(organisation__administrator=self.request.user)
