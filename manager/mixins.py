from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from models import *
from django.core.urlresolvers import reverse
 
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
        
class EntryMixin(LoginRequiredMixin):
    model = Entry
    def get_success_url(self):
        return reverse('entry_list')
    def get_queryset(self):
        return Entry.objects.all()
        
class ListingMixin(LoginRequiredMixin):
    model = Listing
    def get_success_url(self):
        return reverse('listing_list')
    def get_queryset(self):
        return Listing.objects.all()
