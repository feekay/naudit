from django import forms
from teams.models import *
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField
from django.forms.extras.widgets import SelectDateWidget

#Customizing dateinput
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': '', 'autocomplete':'off'}))
    first_name = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'required': ''}))
    last_name = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'required': ''}))
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'required': '' , 'autocomplete':'off'}))
    email= forms.EmailField(widget=forms.EmailInput(attrs={'required': ''}))
    class Meta:
        model = User
        fields= ['first_name','last_name','username', 'email', 'password']

#------------------------------------------------------------------------------#
class MemberForm(forms.ModelForm):

    picture = forms.FileField(widget=forms.FileInput())
    birth_date = forms.DateField(widget=DateInput())
    class Meta:
        model =  Member
        exclude = ['user']

#------------------------------------------------------------------------------#
class TypeForm(forms.Form):
    TYPES = (("e", "Entry Based"),("s","Salary Based"))
    source = forms.ChoiceField(choices = TYPES, widget= forms.RadioSelect(attrs={'required':''}))
    rate = forms.IntegerField(required= False)
    salary = forms.IntegerField(required= False)
    
#------------------------------------------------------------------------------#
    def clean_rate(self):
        data = self.cleaned_data['rate']
        source = self.cleaned_data['source']
        print source
        if source == "e" and not data:
            raise forms.ValidationError("This field is required!")

        return data

#------------------------------------------------------------------------------#        
    def clean_salary(self):
        data = self.cleaned_data['salary']
        source = self.cleaned_data['source']
        if source == "s" and not data:
            raise forms.ValidationError("This field is required!")

        return data
#------------------------------------------------------------------------------#
class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        exclude = []

#------------------------------------------------------------------------------#
class RouteForm(forms.ModelForm):
    route_date =forms.DateField(widget=DateInput())
#Validation implemented in view directly
#    def clean_route_date(self):
#        data = self.cleaned_data['route_date']
#        entries = Entry.objects.filter(route_date = data)
#
#        print entries
#        if not entries:
#            raise forms.ValidationError("No Entry on given date!")
#
#        return data
    class Meta:
        model = Route
        exclude = []
#------------------------------------------------------------------------------#
class AttachmentForm(forms.ModelForm):
    item = forms.FileField(required = False)
    description = forms.CharField(required= False, max_length = 1500, widget=forms.Textarea())

    def clean(self):
        cleaned_data =  super(AttachmentForm, self).clean()
        if cleaned_data['item'] or cleaned_data['description']:
            pass
        else:
            raise forms.ValidationError('Add Text or Image')

    class Meta:
        model = Attachment
        exclude = ['comment', 'key', 'entry', 'used']
#------------------------------------------------------------------------------#
class MyForm(forms.Form):
    file = MultiFileField(min_num=0, max_num=5, max_file_size=1024*1024*5, required = False)
    desc = forms.CharField(required= False, max_length = 1500, widget=forms.Textarea())

#------------------------------------------------------------------------------#
class SettingsForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'required': '', 'autocomplete':'off'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'required': '', 'autocomplete':'off'}))

#------------------------------------------------------------------------------#
class EntryForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    route_date = forms.DateField(widget=DateInput())
    def clean_job_id(self):
    
        """
        Job ID must be unique within a company
        """
        company = self.cleaned_data['company']
        data= self.cleaned_data['job_id']
        try:
            entry = Entry.objects.get(job_id= data, company=company)
        #Change with DoesNotExist
        except Exception:
            #If not found we are good; do nothing
            pass
        else:
            raise forms.ValidationError("Job ID Already exists for current company")

        return data

#------------------------------------------------------------------------------#
    def clean_end_date(self):
        """
        Make sure the End date is always less than the start date
        """
        date_start = self.cleaned_data['start_date']
        date_end = self.cleaned_data['end_date']

        if date_end < date_start:
            raise forms.ValidationError("End date must be greater than start date")

        return date_end

#------------------------------------------------------------------------------#
    def clean_route_date(self):
        """
        Make sure the Route date is always between the start and end date
        """
        
        date_route = self.cleaned_data['route_date']
        
        try:
            date_start = self.cleaned_data['start_date']
            date_end = self.cleaned_data['end_date']

            if date_route > date_end or date_route < date_start:
                raise forms.ValidationError("Route must be between Start and End")

        except:
            pass

        return date_route
#------------------------------------------------------------------------------#
    class Meta:
        model = Entry
        exclude = ["owner", "b_owner", "c_owner", "route", "approved", "visited", "cleared","completed", "verified","finalized", "finalize_date", "teamb_desc","teamc_desc"]

#------------------------------------------------------------------------------#

class CForm(forms.ModelForm):
    comment = forms.CharField(required= False, max_length = 1500, widget=forms.Textarea())
    used = forms.BooleanField(required = False)   
    class Meta:
        model = Attachment
        fields = ['comment', 'used']

