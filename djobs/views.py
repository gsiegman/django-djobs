from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from djobs.forms import JobForm, ContactForm, LocationForm
from djobs.models import Job, JobCategory, Employer
import datetime

def category_jobs(request, slug, **kwargs):
    template_name = kwargs.get("template_name", "djobs/category_jobs.html")
    
    category = get_object_or_404(JobCategory, slug=slug)
    jobs = Job.active.filter(category=category)
    
    return object_list(request, 
        queryset=jobs, 
        allow_empty=True, 
        template_name=template_name, 
        extra_context={'category': category}
    )
    
def employer_jobs(request, id, **kwargs):
    template_name = kwargs.get("template_name", "djobs/employer_jobs.html")
    
    employer = get_object_or_404(Employer, pk=id)
    jobs = Job.active.filter(employer=employer)
    
    return object_list(request, 
        queryset=jobs, 
        allow_empty=True, 
        template_name=template_name, 
        extra_context={'employer': employer}
    )
    
def job_detail(request, id, **kwargs):
    template_name = kwargs.get("template_name", "djobs/job_detail.html")
    
    jobs = Job.active.all()
    
    return object_detail(request, 
        queryset=jobs, 
        object_id=id, 
        template_name=template_name)
        
def create_job(request, **kwargs):
    """
    job creation
    """
    template_name = kwargs.get("template_name", "djobs/job_form.html")
    
    if request.method == 'POST':
        job_form = JobForm(request.POST)
        job_form.fields['employer'].queryset = job_form.fields['employer'].queryset.filter(administrator=request.user)
        
        location_form = LocationForm(request.POST)
        contact_form = ContactForm(request.POST)

        if job_form.is_valid():
            return HttpResponseRedirect(reverse('djobs_index_view'))
    else:
        job_form = JobForm()
        job_form.fields['employer'].queryset = job_form.fields['employer'].queryset.filter(administrator=request.user)
        
        location_form = LocationForm()
        contact_form = ContactForm()

    return render_to_response(template_name, {
            'job_form': job_form,
            'location_form': location_form,
            'contact_form': contact_form,
            'add': True,
        }, context_instance=RequestContext(request)
    )

def edit_job(request, job_id, **kwargs):
    """
    job editing
    """
    template_name = kwargs.get("template_name", "djobs/job_form.html")
    job = get_object_or_404(Job, pk=job_id)
    
    if request.method == 'POST':
        job_form = JobForm(request.POST)
        job_form.fields['employer'].queryset = job_form.fields['employer'].queryset.filter(administrator=request.user)
        
        location_form = LocationForm(request.POST)
        contact_form = ContactForm(request.POST)

        if job_form.is_valid():
            return HttpResponseRedirect(reverse('djobs_index_view'))
        
        if form.is_valid():
            return HttpResponseRedirect(reverse('djobs_index_view'))
    else:
        job_form = JobForm({'title': job.title, 'description': job.description,
            'category': job.category.id,
            'employment_type': job.employment_type,
            'employment_level': job.employment_level,
            'employer': job.employer.id,
        })
        job_form.fields['employer'].queryset = job_form.fields['employer'].queryset.filter(administrator=request.user)
        
        location_form = LocationForm()
        contact_form = ContactForm()
        
    return render_to_response(template_name, {
            'job_form': job_form,
            'location_form': location_form,
            'contact_form': contact_form,
            'add': False,
        }, context_instance=RequestContext(request)
    )