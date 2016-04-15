from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *
from manager.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Init dajax
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'clubmanager.views.home', name='home'),
    # url(r'^clubmanager/', include('clubmanager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),    
    (r'^$', 'manager.views.main_menu'),
    
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Login / logout.
    (r'^login/$', 
     'django.contrib.auth.views.login', 
     {'template_name': 'accounts/login.html'}),
    
    (r'^logout/$', 'manager.views.logout_page'),
    
    (r'^password_change/$', 
     'django.contrib.auth.views.password_change', 
     {'template_name': 'accounts/password_change_form.html'}),

    (r'^password_change/done/$', 
     'django.contrib.auth.views.password_change_done', 
     {'template_name': 'accounts/password_change_done.html'}),

    (r'^password_reset/$', 
     'django.contrib.auth.views.password_reset', 
     {'template_name': 'accounts/password_reset_form.html',
      'email_template_name': 'accounts/password_reset_email.html'}),

    (r'^password_reset/done/$', 
     'django.contrib.auth.views.password_reset_done', 
     {'template_name': 'accounts/password_reset_done.html'}),

    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
     'django.contrib.auth.views.password_reset_confirm', 
     {'template_name': 'accounts/password_reset_confirm.html'}),

    (r'^reset/done/$', 
     'django.contrib.auth.views.password_reset_complete', 
     {'template_name': 'accounts/password_reset_complete.html'}),

    (r'^signup/$', 
     'manager.views.signup', 
     {'template_name': 'accounts/signup_form.html',
      'email_template_name': 'accounts/signup_email.html'}),

    (r'^signup/done/$', 
     'manager.views.signup_done', 
     {'template_name': 'accounts/signup_done.html'}),

    (r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
     'manager.views.signup_confirm'),

    (r'^signup/complete/$', 
     'manager.views.signup_complete', 
     {'template_name': 'accounts/signup_complete.html'}),
                        
    url (
       regex = '^entry/list/$',
       view =  EntryListView.as_view(),
       name = 'entry_list'
     ),

    url (
        regex = '^entry/create/$',
        view =  EntryCreateView.as_view(),
        name = 'entry_create'
    ),

    url (
        regex = '^entry/detail/(?P<pk>\d+)/$',
        view =  EntryDetailView.as_view(),
        name = 'entry_detail'
    ),
    
    url (
        regex = '^entry/delete/(?P<pk>\d+)/$',
        view =  EntryDeleteView.as_view(),
        name = 'entry_delete'
    ),
    
    url (
        regex = '^entry/update/(?P<pk>\d+)/$',
        view =  EntryUpdateView.as_view(),
        name = 'entry_update'
    ),

    url (
       regex = '^listing/list/$',
       view =  ListingListView.as_view(),
       name = 'listing_list'
     ),

    url (
        regex = '^listing/create/$',
        view =  ListingCreateView.as_view(),
        name = 'listing_create'
    ),

    url (
        regex = '^listing/detail/(?P<pk>\d+)/$',
        view =  ListingDetailView.as_view(),
        name = 'listing_detail'
    ),
    
    url (
        regex = '^listing/delete/(?P<pk>\d+)/$',
        view =  ListingDeleteView.as_view(),
        name = 'listing_delete'
    ),
    
    url (
        regex = '^listing/update/(?P<pk>\d+)/$',
        view =  ListingUpdateView.as_view(),
        name = 'listing_update'
    ),

    url(r'^search/$', search),    
    url(r'^upload_file/$', upload_file),    
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
