from django import forms
from djobs.models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job