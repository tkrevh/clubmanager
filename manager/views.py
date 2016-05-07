# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from django.db.models import Count, Max, Min, Sum, Avg
from manager.mixins import *
from manager.forms import *
from manager.models import *
from datetime import timedelta, date, datetime
from django.db.models import Q
    
@login_required
def main_menu(request):
    try:
      organisation = Organisation.objects.get(administrator=request.user)
    except Organisation.DoesNotExist:
      organisation = None
    return render_to_response('mainmenu.html',{'organisation':organisation,}, context_instance=RequestContext(request))    
  
@login_required
def reports_menu(request):
    try:
      organisation = Organisation.objects.get(administrator=request.user)
    except Organisation.DoesNotExist:
      organisation = None
    return render_to_response('reports.html',{'organisation':organisation,}, context_instance=RequestContext(request))    
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')    
    
@csrf_protect
def signup(request, template_name='registration/signup.html', 
           email_template_name='registration/signup_email.html',
           signup_form=UserCreationForm,
           token_generator=default_token_generator,
           post_signup_redirect=None):
    if post_signup_redirect is None:
        post_signup_redirect = reverse('manager.views.signup_done')
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            if not Site._meta.installed:
                opts['domain_override'] = RequestSite(request).domain
            form.save(**opts)
            return HttpResponseRedirect(post_signup_redirect)
    else:
        form = signup_form()
    return render_to_response(template_name, {'form': form,}, 
                              context_instance=RequestContext(request))

def signup_done(request, template_name='registration/signup_done.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request))

def signup_confirm(request, uidb36=None, token=None,
                   token_generator=default_token_generator,
                   post_signup_redirect=None):
    assert uidb36 is not None and token is not None #checked par url
    if post_signup_redirect is None:
        post_signup_redirect = reverse('manager.views.signup_complete')
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        user.is_active = True
        user.save()
    else:
        context_instance['validlink'] = False
    return HttpResponseRedirect(post_signup_redirect)

def signup_complete(request, template_name='registration/signup_complete.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request, 
                                                              {'login_url': settings.LOGIN_URL}))    
    
class AircraftListView(AircraftMixin, ListView):
    pass

class AircraftDetailView(AircraftMixin, DetailView):
    pass

class AircraftCreateView(AircraftMixin, CreateView):
    form_class = AircraftForm
    succes_url = 'aircraft_list'
    template_name = 'manager/aircraft_create.html'

    def get_context_data(self, **kwargs):
        return super(AircraftCreateView, self).get_context_data(**kwargs)
        
    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(administrator=self.request.user)
        return super(AircraftCreateView, self).form_valid(form)        
        

class AircraftDeleteView(AircraftMixin, DeleteView):
    pass

class AircraftUpdateView(AircraftMixin, UpdateView):
    form_class = AircraftForm
    succes_url = 'aircraft_list'
    template_name = 'manager/aircraft_create.html'
    

class MemberListView(MemberMixin, ListView):
    pass

class MemberDetailView(MemberMixin, DetailView):
    pass

class MemberCreateView(MemberMixin, CreateView):
    form_class = MemberForm
    succes_url = 'member_list'
    template_name = 'manager/member_create.html'

    def get_context_data(self, **kwargs):
        return super(MemberCreateView, self).get_context_data(**kwargs)
        
    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(administrator=self.request.user)
        userName = '%s' % form.instance.email.split('@',1)[0]
        userPass = form.instance.email
        userMail = form.instance.email
        userFirstName = form.instance.first_name
        userLastName = form.instance.last_name

        # TODO: check if already existed
        if userName and userPass and userMail:
           user,created = User.objects.get_or_create(username=userName, email=userMail)
           if created:
              # user was created, set pwd
              user.set_password(userPass)
              user.first_name = userFirstName
              user.last_name = userLastName
              
        form.instance.user = user
        return super(MemberCreateView, self).form_valid(form)        

class MemberDeleteView(MemberMixin, DeleteView):
    pass

class MemberUpdateView(MemberMixin, UpdateView):
    form_class = MemberForm
    succes_url = 'member_list'
    template_name = 'manager/member_create.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(MemberUpdateView, self).get_context_data(**kwargs)
        ctx['member'] = Member.objects.filter(pk=self.kwargs['pk'])
        return ctx

class DocumentListView(DocumentMixin, ListView):
    pass

class DocumentDetailView(DocumentMixin, DetailView):
    pass

class DocumentCreateView(DocumentMixin, CreateView):
    form_class = DocumentForm
    succes_url = 'member_update'
    
    def get_success_url(self):
        return reverse('member_update', kwargs={'pk': self.kwargs['member_id']}) 

    def get_context_data(self, **kwargs):
        return super(DocumentCreateView, self).get_context_data(**kwargs)
        
    def form_valid(self, form):
        form.instance.member_id = self.kwargs['member_id']
        return super(DocumentCreateView, self).form_valid(form)        

class DocumentDeleteView(DocumentMixin, DeleteView):
    pass

class DocumentUpdateView(DocumentMixin, UpdateView):
    form_class = DocumentForm
    succes_url = 'member_update'
    
    def get_success_url(self):
        return reverse('member_update', kwargs={'pk': self.kwargs['member_id']}) 
    
    def get_context_data(self, **kwargs):
        ctx = super(DocumentUpdateView, self).get_context_data(**kwargs)
        ctx['member_id'] =  self.kwargs['member_id']
        return ctx

        
class OrganisationDetailView(OrganisationMixin, DetailView):
    pass

class OrganisationCreateView(OrganisationMixin, CreateView):
    form_class = OrganisationForm
    succes_url = 'organisation_create'
    template_name = 'manager/organisation_create.html'

    def get_context_data(self, **kwargs):
        return super(OrganisationCreateView, self).get_context_data(**kwargs)
        
    def form_valid(self, form):
        form.instance.administrator = self.request.user
        return super(OrganisationCreateView, self).form_valid(form)        

class OrganisationUpdateView(OrganisationMixin, UpdateView):
    form_class = OrganisationForm
    succes_url = '/'
    template_name = 'manager/organisation_update.html'
    
    
class LogbookListView(LogbookMixin, ListView):
    paginate_by = 30
    def get_context_data(self, **kwargs):
        ctx = super(LogbookListView, self).get_context_data(**kwargs)
        ctx['type'] = self.kwargs['type']
        return ctx
    
class LogbookDeleteView(LogbookMixin, DeleteView):
    pass
    
class LogbookDetailView(LogbookMixin, DetailView):
    pass

class LogbookCreateView(LogbookMixin, CreateView):
    form_class = LogbookForm
    succes_url = 'logbook_list'
    template_name = 'manager/logbook_create.html'

    def get_context_data(self, **kwargs):
        ctx = super(LogbookCreateView, self).get_context_data(**kwargs)
        ctx['type'] = self.kwargs['type']
        return ctx
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.organisation = Organisation.objects.get(administrator=self.request.user)
        self.object.type = self.kwargs['type']
        
        try:
            self.object.full_clean()
        except ValidationError:
            return self.form_invalid(form)

        return super(LogbookCreateView, self).form_valid(form) 
    
    def form_invalid(self, form):
        from django.forms.util import ErrorList
        form._errors["date"] = ErrorList([_("Logbook for this date already exists !")])
        return super(LogbookCreateView, self).form_invalid(form)   
   

class LogbookUpdateView(LogbookMixin, UpdateView):
    form_class = LogbookForm
    succes_url = '/'
    template_name = 'manager/logbook_update.html'


# the main view for flight entry    
class LogbookManageView(FlightMixin, CreateView):
    template_name = 'manager/logbook_manage.html'
    form_class = SailplaneFlightForm
    
    def get_context_data(self, **kwargs):
        ctx = super(LogbookManageView, self).get_context_data(**kwargs)
        logbook_type=self.kwargs['type']
        logbook_id=self.kwargs['logbook_id']
        ctx['flights'] = Flight.objects.filter(logbook__organisation__administrator=self.request.user).filter(logbook__type=logbook_type).filter(logbook__pk=logbook_id)
        ctx['logbook'] = Logbook.objects.filter(pk=logbook_id)[0]
        ctx['type'] = self.kwargs['type']
        return ctx
        
    def get_form(self, form_class):
        if self.kwargs['type'] == 'sailplane':
            form_class = SailplaneFlightForm
        else:
            form_class = PoweredAircraftFlightForm
        form = super(LogbookManageView, self).get_form(form_class)
        return form        
    
    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(administrator=self.request.user)
        logbook_id = self.kwargs['logbook_id']
        logbook = Logbook.objects.filter(pk=logbook_id)[0]
        form.instance.logbook = logbook
        return super(LogbookManageView, self).form_valid(form)        

# the main view for flight entry    
class LogbookManageAdvancedView(FlightMixin, CreateView):
    template_name = 'manager/logbook_manage_advanced.html'
    form_class = SailplaneFlightForm
    
    def get_context_data(self, **kwargs):
        ctx = super(LogbookManageAdvancedView, self).get_context_data(**kwargs)
        logbook_type=self.kwargs['type']
        logbook_id=self.kwargs['logbook_id']
        ctx['flights'] = Flight.objects.filter(logbook__organisation__administrator=self.request.user).filter(logbook__type=logbook_type).filter(logbook__pk=logbook_id).order_by('pk')
        ctx['logbook'] = Logbook.objects.filter(pk=logbook_id)[0]
        ctx['type'] = self.kwargs['type']
        return ctx
        
    def get_form(self, form_class):
        if self.kwargs['type'] == 'sailplane':
            form_class = SailplaneFlightForm
        else:
            form_class = PoweredAircraftFlightForm
        form = super(LogbookManageAdvancedView, self).get_form(form_class)
        return form        
    
    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(administrator=self.request.user)
        logbook_id = self.kwargs['logbook_id']
        logbook = Logbook.objects.filter(pk=logbook_id)[0]
        form.instance.logbook = logbook
        return super(LogbookManageAdvancedView, self).form_valid(form)        

# report views
def list_flight_years_allmembers(request, type):
    years_list = Flight.objects.filter(aircraft__type=type).dates('date', 'year', order='DESC')
    return render_to_response('manager/reports/report_list_years_allmembers.html', {'object_list': years_list, 'type': type}, context_instance=RequestContext(request))
        
# lists number of flights and total time for each member in a year
def report_members_yearly(request, type, year):
    report = Flight.objects.filter(date__year=year).filter(aircraft__type=type).values('first_name','last_name').annotate(total_flight_time=Sum('flight_time')).annotate(num_flights=Count('pilot')).order_by('-total_flight_time')
    return render_to_response('manager/reports/report_members_yearly.html', {'object_list': report, 'type': type, 'year': year}, context_instance=RequestContext(request))
        
# report views
def list_flight_years_bytype(request, type):
    years_list = Flight.objects.filter(aircraft__type=type).dates('date', 'year', order='DESC')
    return render_to_response('manager/reports/report_list_years_bytype.html', {'object_list': years_list, 'type': type}, context_instance=RequestContext(request))
        
# lists number of flights and total time for each member in a year
def report_bytype_yearly(request, type, year):
    report = Flight.objects.filter(date__year=year).filter(aircraft__type=type).values('model','registration').annotate(total_flight_time=Sum('flight_time')).annotate(num_flights=Count('pilot')).order_by('-total_flight_time')
    return render_to_response('manager/reports/report_bytype_yearly.html', {'object_list': report, 'type': type, 'year': year}, context_instance=RequestContext(request))
    
def report_detailed(request, type):
   if request.method == 'POST':
      form = DetailReportForm(request.POST)
      isvalid = form.is_valid()
      report = Flight.objects.filter(aircraft__type=type)
      if form.data['pilot']:
         report = report.filter(Q(pilot__pk=int(form.data['pilot'])) | Q(instructor__pk=int(form.data['pilot'])))
      if form.data['aircraft']:
         report = report.filter(aircraft__pk=int(form.data['aircraft']))
      if form.data['date_from']:
         report = report.filter(date__gte=datetime.strptime(form.data['date_from'], '%d/%m/%Y'))
      if form.data['date_to']:
         report = report.filter(date__lte=datetime.strptime(form.data['date_to'], '%d/%m/%Y'))
      if form.data['text_search']:
         query = form.data['text_search']
         report = report.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(model__icontains=query) | Q(registration__icontains=query) | Q(aircraft__competition_number=query))

      summary_per_aircraft = report.values('aircraft', 'registration', 'model').annotate(num_flights=Count('aircraft')).annotate(total_flight_time=Sum('flight_time'))
      
      summary_per_aircraft_noncommercial = report.filter(purpose__billing_type='noncommercial').values('aircraft', 'registration', 'model', 'purpose__billing_type').annotate(num_flights=Count('aircraft')).annotate(total_flight_time=Sum('flight_time'))
      summary_per_aircraft_commercial = report.filter(purpose__billing_type='commercial').values('aircraft', 'registration', 'model', 'purpose__billing_type').annotate(num_flights=Count('aircraft')).annotate(total_flight_time=Sum('flight_time'))

      report = report.order_by('-date', '-time_takeoff')
      total_time = report.aggregate(total_flight_time=Sum('flight_time'))['total_flight_time']

      if report.count() > 1000:
         report = report[:1000]

      return render_to_response('manager/reports/report_detailed.html', {'report': report, 'num_flights': report.count(), 'total_time': total_time, 'summary_per_aircraft': summary_per_aircraft, 'summary_per_aircraft_noncommercial': summary_per_aircraft_noncommercial, 'summary_per_aircraft_commercial': summary_per_aircraft_commercial, 'form': form, 'type': type}, context_instance=RequestContext(request))
   else:
      form = DetailReportForm()

   return render_to_response('manager/reports/report_detailed.html', {'form': form, 'type': type}, context_instance=RequestContext(request))
    
# the main view for flight entry    
class FlightCreateView(FlightMixin, CreateView):
    form_class = SailplaneFlightForm
    template_name = 'manager/flight_form.html'
    success_url = 'logbook_manage'
    
    def get_context_data(self, **kwargs):
        ctx = super(FlightCreateView, self).get_context_data(**kwargs)
        logbook_type=self.kwargs['type']
        logbook_id=self.kwargs['logbook_id']
        ctx['flights'] = Flight.objects.filter(logbook__organisation__administrator=self.request.user).filter(logbook__type=logbook_type).filter(logbook__pk=logbook_id)
        ctx['logbook'] = Logbook.objects.filter(pk=logbook_id)[0]
        ctx['type'] = self.kwargs['type']
        return ctx
        
    def get_form(self, form_class):
        if self.kwargs['type'] == 'sailplane':
            form_class = SailplaneFlightForm
        else:
            form_class = PoweredAircraftFlightForm
        form = super(FlightCreateView, self).get_form(form_class)
        form.fields["aircraft"].queryset = Aircraft.objects.filter(type=self.kwargs['type'])
        return form        
    
    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(administrator=self.request.user)
        logbook_id = self.kwargs['logbook_id']
        logbook = Logbook.objects.filter(pk=logbook_id)[0]
        form.instance.logbook = logbook
        
        # copy pilot data
        if not form.instance.first_name:
            form.instance.first_name = form.instance.pilot.first_name
        if not form.instance.last_name:
            form.instance.last_name = form.instance.pilot.last_name

        # copy instructor data
        if form.instance.instructor:
           if not form.instance.instructor_first_name:
               form.instance.instructor_first_name = form.instance.instructor.first_name
           if not form.instance.instructor_last_name:
               form.instance.instructor_last_name = form.instance.instructor.last_name
        
        # copy aircraft data
        if not form.instance.make:
            form.instance.make = form.instance.aircraft.make
        if not form.instance.model:
            form.instance.model = form.instance.aircraft.model
        if not form.instance.registration:
            form.instance.registration = form.instance.aircraft.registration
        if not form.instance.serial_number:
            form.instance.serial_number = form.instance.aircraft.serial_number
        
        return super(FlightCreateView, self).form_valid(form)       

class AdvancedFlightCreateView(FlightCreateView):       

   def get_success_url(self):
      return reverse('logbook_manage_advanced', kwargs={'type': self.kwargs['type'], 'logbook_id': self.kwargs['logbook_id']}) 
    
class FlightUpdateView(FlightMixin, UpdateView):
    form_class = SailplaneFlightForm
    template_name = 'manager/flight_form.html'

    def get_success_url(self):
        return reverse('logbook_manage', kwargs={'type': self.kwargs['type'], 'logbook_id': self.kwargs['logbook_id']}) 
    
    def get_form(self, form_class):
        if self.kwargs['type'] == 'sailplane':
            form_class = SailplaneFlightForm
        else:
            form_class = PoweredAircraftFlightForm
        form = super(FlightUpdateView, self).get_form(form_class)
        form.fields["aircraft"].queryset = Aircraft.objects.filter(type=self.kwargs['type'])
        return form        
        
    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(administrator=self.request.user)
        logbook_id = self.kwargs['logbook_id']
        logbook = Logbook.objects.filter(pk=logbook_id)[0]
        form.instance.logbook = logbook
        
        # set pilot data
        form.instance.first_name = form.instance.pilot.first_name
        form.instance.last_name = form.instance.pilot.last_name

        # set/reset instructor data
        if not form.instance.instructor:
            form.instance.instructor_first_name = ""
            form.instance.instructor_last_name = ""
            form.instance.instructor = None
        else:
            form.instance.instructor_first_name = form.instance.instructor.first_name
            form.instance.instructor_last_name = form.instance.instructor.last_name
        
        # set aircraft data
        form.instance.make = form.instance.aircraft.make
        form.instance.model = form.instance.aircraft.model
        form.instance.registration = form.instance.aircraft.registration
        form.instance.serial_number = form.instance.aircraft.serial_number
        
        return super(FlightUpdateView, self).form_valid(form)        
        
class AdvancedFlightUpdateView(FlightUpdateView):

   def get_success_url(self):
      return reverse('logbook_manage_advanced', kwargs={'type': self.kwargs['type'], 'logbook_id': self.kwargs['logbook_id']}) 

class FlightDeleteView(FlightMixin, DeleteView):
   pass    
   
class AdvancedFlightDeleteView(FlightMixinAdvanced, DeleteView):
   pass
   
class PurposeListView(PurposeMixin, ListView):
    pass

class PurposeDetailView(PurposeMixin, DetailView):
    pass

class PurposeCreateView(PurposeMixin, CreateView):
    form_class = PurposeForm
    succes_url = 'purpose_list'
    template_name = 'manager/purpose_create.html'

    def get_context_data(self, **kwargs):
        return super(PurposeCreateView, self).get_context_data(**kwargs)
        
    def form_valid(self, form):
        form.instance.organisation = Organisation.objects.get(administrator=self.request.user)
        return super(PurposeCreateView, self).form_valid(form)        
        

class PurposeDeleteView(PurposeMixin, DeleteView):
    pass

class PurposeUpdateView(PurposeMixin, UpdateView):
    form_class = PurposeForm
    succes_url = 'purpose_list'
    template_name = 'manager/purpose_update.html'
   