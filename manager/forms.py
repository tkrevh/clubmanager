from datetime import date
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.template import Context, loader
from django import forms
from django.core.mail import send_mail
from manager.models import *
    
def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.input_formats = ('%d/%m/%Y',)
        formfield.widget.format = '%d/%m/%Y'
        formfield.widget.attrs.update({'class':'datePicker'})
    if isinstance(f, models.TimeField):
        formfield.widget.attrs.update({'class':'timePicker'})
    return formfield    
    
class UserCreationForm(forms.ModelForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
                                error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput, help_text = _("Enter the same password as above, for verification."))
    email1 = forms.EmailField(label=_("Email"), max_length=75)
    email2 = forms.EmailField(label=_("Email confirmation"), max_length=75, help_text = _("Enter your email address again. A confirmation email will be sent to this address."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
    def clean_email1(self):
        email1 = self.cleaned_data["email1"]
        users_found = User.objects.filter(email__iexact=email1)
        if len(users_found) >= 1:
            raise forms.ValidationError(_("A user with that email already exist."))
        return email1

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1", "")
        email2 = self.cleaned_data["email2"]
        if email1 != email2:
            raise forms.ValidationError(_("The two email fields didn't match."))
        return email2

    def save(self, commit=True, domain_override=None,
             email_template_name='registration/signup_email.html',
             use_https=False, token_generator=default_token_generator):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email1"]
        user.is_active = False
        if commit:
            user.save()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
            }
        send_mail("Confirmation link sent on %s" % site_name,
                  t.render(Context(c)), 'tadej.krevh@gmail.com', [user.email])
        return user    
    
class AircraftForm(ModelForm):

    class Meta:
        model = Aircraft
        exclude = ('organisation')

class MemberForm(ModelForm):
    formfield_callback = make_custom_datefield
    class Meta:
        model = Member
        exclude = ('organisation', 'date_joined', 'last_login', 'last_password_check', 'user')
          
class DocumentForm(ModelForm):
    formfield_callback = make_custom_datefield
    class Meta:
        model = Document
        exclude = ('member')
          
class OrganisationForm(ModelForm):

    class Meta:
        model = Organisation
        exclude = ('administrator')
        
        
class LogbookForm(ModelForm):
    formfield_callback = make_custom_datefield
    class Meta:
        model = Logbook
        exclude = ('organisation', 'type')
        
    def clean_date(self):
        submited_date  = self.cleaned_data['date']

        if submited_date:
            existingLogbook = Logbook.objects.filter(type=self.instance.type, date=submited_date)
            if existingLogbook:
                raise forms.ValidationError(_("Logbook already exists for this type and date!"))

        # Always return the full collection of cleaned data.
        return submited_date     
        
class SailplaneFlightForm(ModelForm):
    time_takeoff = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
    time_tow_release = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
    time_landing = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
    
    remark = forms.CharField( widget=forms.Textarea, required=False )
    
    formfield_callback = make_custom_datefield
    
    class Meta:
        model = Flight
        exclude = ('organisation', 'logbook', 'time_block_off', 'time_block_on', 'date', 'flight_time')

class PoweredAircraftFlightForm(ModelForm):
    time_block_off = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
    time_takeoff = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
    time_tow_release = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
    time_landing = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
    time_block_on = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class':'timePicker'}), input_formats = ('%H:%M',), required=False )
   
    remark = forms.CharField( widget=forms.Textarea, required=False )

    formfield_callback = make_custom_datefield
    
    class Meta:
        model = Flight
        exclude = ('organisation', 'logbook', 'igc_file', 'time_tow_release', 'date', 'flight_time')
                
class PurposeForm(ModelForm):

    class Meta:
        model = Purpose
        exclude = ('organisation')
                
                

class DetailReportForm(forms.Form):
    formfield_callback = make_custom_datefield

    pilot = forms.IntegerField(required=False)
    aircraft = forms.IntegerField(required=False)
    date_from = forms.DateField(input_formats = ('%d/%m/%Y',), required=False)
    date_to = forms.DateField(input_formats = ('%d/%m/%Y',), required=False)
    text_search = forms.CharField(required=False)
    
    
    
    
    
    
    
    