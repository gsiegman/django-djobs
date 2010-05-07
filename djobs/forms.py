from django import forms
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.utils.translation import ugettext_lazy as _
from djobs.models import Job, JobCategory, Employer, \
    Location, Contact, EMPLOYMENT_TYPE_CHOICES, EMPLOYMENT_LEVEL_CHOICES

class JobForm(forms.Form):
    title = forms.CharField(max_length=50,
        help_text=_("Max 50 chars. Required.")
    )
    description = forms.CharField(widget=forms.widgets.Textarea,
        help_text=_("Required.")
    )
    category = forms.ModelChoiceField(queryset=JobCategory.objects.all())
    employment_type = forms.ChoiceField(EMPLOYMENT_TYPE_CHOICES)
    employment_level = forms.ChoiceField(EMPLOYMENT_LEVEL_CHOICES)
    employer = forms.ModelChoiceField(queryset=Employer.objects.all())
        
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100, 
        help_text=_('Required.')
    )
    
    class Meta:
        model = Contact
    