# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
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
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import logging

logger = logging.getLogger(__name__)
    
@login_required
def main_menu(request):
    return render_to_response('mainmenu.html',{}, context_instance=RequestContext(request))    
  
@login_required
def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            entries = Entry.objects.filter(name__istartswith=q)
            return render(request, 'search_results.html', {'entries': entries, 'query': q})
    return render(request, 'mainmenu.html', {'errors': errors})  
        
def handle_uploaded_file(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams(line_overlap=0.5,
                        char_margin=2.0,
                        line_margin=4.0,
                        word_margin=0.1,
                        boxes_flow=0.5,
                        detect_vertical=False,
                        all_texts=True)
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(pdf_file, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    pdf_file.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str  

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug('Uploaded file: %s' % request.FILES['file'])
            #return render(request, 'manager/display_pdf.html', {'pdf_to_html': handle_uploaded_file(request.FILES['file'])})
            return HttpResponse(handle_uploaded_file(request.FILES['file']))
            #return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    #return render_to_response('manager/file_upload.html', {'form': form})    
    return render(request, 'manager/file_upload.html', {'form': form})  
        
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
    
class EntryListView(EntryMixin, ListView):
    pass

class EntryDetailView(EntryMixin, DetailView):
    pass

class EntryCreateView(EntryMixin, CreateView):
    form_class = EntryForm
    succes_url = 'entry_list'
    template_name = 'manager/entry_create.html'

    def get_context_data(self, **kwargs):
        return super(EntryCreateView, self).get_context_data(**kwargs)
        
    def form_valid(self, form):
        return super(EntryCreateView, self).form_valid(form)        
        

class EntryDeleteView(EntryMixin, DeleteView):
    pass

class EntryUpdateView(EntryMixin, UpdateView):
    form_class = EntryForm
    succes_url = 'entry_list'
    template_name = 'manager/entry_create.html'
    

class ListingListView(ListingMixin, ListView):
    pass

class ListingDetailView(ListingMixin, DetailView):
    pass

class ListingCreateView(ListingMixin, CreateView):
    form_class = ListingForm
    succes_url = 'listing_list'
    template_name = 'manager/listing_create.html'

    def get_context_data(self, **kwargs):
        return super(ListingCreateView, self).get_context_data(**kwargs)
        
    def form_valid(self, form):
        return super(ListingCreateView, self).form_valid(form)        

class ListingDeleteView(ListingMixin, DeleteView):
    pass

class ListingUpdateView(ListingMixin, UpdateView):
    form_class = ListingForm
    succes_url = 'listing_list'
    template_name = 'manager/listing_create.html'
    
    def get_context_data(self, **kwargs):
        return super(ListingUpdateView, self).get_context_data(**kwargs)

