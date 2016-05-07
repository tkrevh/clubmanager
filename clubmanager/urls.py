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
    
    (r'^reports/$', 'manager.views.reports_menu'),
    (r'^reports/(?P<type>\w+)/allmembers/$', 'manager.views.list_flight_years_allmembers'),
    (r'^reports/(?P<type>\w+)/allmembers/(?P<year>\d+)/$', 'manager.views.report_members_yearly'),
    
    (r'^reports/(?P<type>\w+)/bytype/$', 'manager.views.list_flight_years_bytype'),
    (r'^reports/(?P<type>\w+)/bytype/(?P<year>\d+)/$', 'manager.views.report_bytype_yearly'),
    
    (r'^reports/(?P<type>\w+)/detailed/$', 'manager.views.report_detailed'),

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
       regex = '^aircraft/list/$',
       view =  AircraftListView.as_view(),
       name = 'aircraft_list'
     ),

    url (
        regex = '^aircraft/create/$',
        view =  AircraftCreateView.as_view(),
        name = 'aircraft_create'
    ),

    url (
        regex = '^aircraft/detail/(?P<pk>\d+)/$',
        view =  AircraftDetailView.as_view(),
        name = 'aircraft_detail'
    ),
    
    url (
        regex = '^aircraft/delete/(?P<pk>\d+)/$',
        view =  AircraftDeleteView.as_view(),
        name = 'aircraft_delete'
    ),
    
    url (
        regex = '^aircraft/update/(?P<pk>\d+)/$',
        view =  AircraftUpdateView.as_view(),
        name = 'aircraft_update'
    ),

    url (
       regex = '^purpose/list/$',
       view =  PurposeListView.as_view(),
       name = 'purpose_list'
     ),

    url (
        regex = '^purpose/create/$',
        view =  PurposeCreateView.as_view(),
        name = 'purpose_create'
    ),

    url (
        regex = '^purpose/detail/(?P<pk>\d+)/$',
        view =  PurposeDetailView.as_view(),
        name = 'purpose_detail'
    ),
    
    url (
        regex = '^purpose/delete/(?P<pk>\d+)/$',
        view =  PurposeDeleteView.as_view(),
        name = 'purpose_delete'
    ),
    
    url (
        regex = '^purpose/update/(?P<pk>\d+)/$',
        view =  PurposeUpdateView.as_view(),
        name = 'purpose_update'
    ),
    
    url (
       regex = '^member/list/$',
       view =  MemberListView.as_view(),
       name = 'member_list'
     ),

    url (
        regex = '^member/create/$',
        view =  MemberCreateView.as_view(),
        name = 'member_create'
    ),

    url (
        regex = '^member/detail/(?P<pk>\d+)/$',
        view =  MemberDetailView.as_view(),
        name = 'member_detail'
    ),
    
    url (
        regex = '^member/delete/(?P<pk>\d+)/$',
        view =  MemberDeleteView.as_view(),
        name = 'member_delete'
    ),
    
    url (
        regex = '^member/update/(?P<pk>\d+)/$',
        view =  MemberUpdateView.as_view(),
        name = 'member_update'
    ),
    
    url (
       regex = '^logbook/(?P<type>\w+)/list/$',
       view =  LogbookListView.as_view(),
       name = 'logbook_list'
     ),

    url (
        regex = '^logbook/(?P<type>\w+)/create/$',
        view =  LogbookCreateView.as_view(),
        name = 'logbook_create'
    ),

    url (
        regex = '^logbook/(?P<type>\w+)/detail/(?P<pk>\d+)/$',
        view =  LogbookDetailView.as_view(),
        name = 'logbook_detail'
    ),
    
    url (
        regex = '^logbook/delete/(?P<pk>\d+)/$',
        view =  LogbookDeleteView.as_view(),
        name = 'logbook_delete'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/update/(?P<pk>\d+)/$',
        view =  LogbookUpdateView.as_view(),
        name = 'logbook_update'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/manage/(?P<logbook_id>\d+)/$',
        view =  LogbookManageView.as_view(),
        name = 'logbook_manage'
    ),

    url (
        regex = '^logbook/(?P<type>\w+)/manage/advanced/(?P<logbook_id>\d+)/$',
        view =  LogbookManageAdvancedView.as_view(),
        name = 'logbook_manage_advanced'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/manage/(?P<logbook_id>\d+)/create/flight/$',
        view =  FlightCreateView.as_view(),
        name = 'flight_create'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/manage/(?P<logbook_id>\d+)/create/flight/advanced/$',
        view =  AdvancedFlightCreateView.as_view(),
        name = 'flight_create_advanced'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/manage/(?P<logbook_id>\d+)/edit/flight/(?P<pk>\d+)/$',
        view =  FlightUpdateView.as_view(),
        name = 'flight_create'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/manage/(?P<logbook_id>\d+)/edit/flight/advanced/(?P<pk>\d+)/$',
        view =  AdvancedFlightUpdateView.as_view(),
        name = 'flight_update_advanced'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/manage/(?P<logbook_id>\d+)/delete/flight/(?P<pk>\d+)/$',
        view =  FlightDeleteView.as_view(),
        name = 'flight_delete'
    ),
    
    url (
        regex = '^logbook/(?P<type>\w+)/manage/(?P<logbook_id>\d+)/delete/flight/advanced/(?P<pk>\d+)/$',
        view =  AdvancedFlightDeleteView.as_view(),
        name = 'flight_delete_advanced'
    ),
    
    url (
        regex = '^organisation/create/$',
        view =  OrganisationCreateView.as_view(),
        name = 'organisation_create'
    ),

    url (
        regex = '^organisation/update/(?P<pk>\d+)/$',
        view =  OrganisationUpdateView.as_view(),
        name = 'organisation_update'
    ),
    
    url (
        regex = '^document/create/(?P<member_id>\d+)/$',
        view =  DocumentCreateView.as_view(),
        name = 'document_create'
    ),

    url (
        regex = '^document/update/(?P<member_id>\d+)/(?P<pk>\d+)/$',
        view =  DocumentUpdateView.as_view(),
        name = 'document_update'
    ),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
