from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from djobs.forms import JobForm, ContactForm, LocationForm, EmployerForm
from djobs.models import Job, JobCategory, Employer, EmployerLogo, Location
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
        location_form = LocationForm(request.POST)
        
        if location_form.is_valid():
            location = location_form.save()
        
        contact_form = ContactForm(request.POST)
        
        if contact_form.is_valid():
            contact = contact_form.save()
        
        job_form = JobForm(request.POST)
        job_form.fields['employer'].queryset = job_form.fields['employer'].queryset.filter(administrator=request.user)
        
        if job_form.is_valid():
            title = job_form.cleaned_data['title']
            description = job_form.cleaned_data['description']
            category = job_form.cleaned_data['category']
            employment_type = job_form.cleaned_data['employment_type']
            employment_level = job_form.cleaned_data['employment_level']
            employer = job_form.cleaned_data['employer']
            
            new_job = Job.objects.create(title=title,
                description=description,
                category=category,
                employment_type=employment_type,
                employment_level=employment_level,
                employer=employer,
                location=location,
                contact=contact
            )
            
            return HttpResponseRedirect(reverse('djobs_edit_job',
                args=[new_job.id]
            ))
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

    if request.user != job.employer.administrator:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        
        if location_form.is_valid():
            job.location = location_form.save()
        
        contact_form = ContactForm(request.POST)
        
        if contact_form.is_valid():
            job.contact = contact_form.save()
        
        job_form = JobForm(request.POST)
        job_form.fields['employer'].queryset = job_form.fields['employer'].queryset.filter(administrator=request.user)
        
        if job_form.is_valid():
            job.title = job_form.cleaned_data['title']
            job.description = job_form.cleaned_data['description']
            job.category = job_form.cleaned_data['category']
            job.employment_type = job_form.cleaned_data['employment_type']
            job.employment_level = job_form.cleaned_data['employment_level']
            job.employer = job_form.cleaned_data['employer']
            
            job.save()
            
            return HttpResponseRedirect(reverse('djobs_edit_job',
                args=[job.id]
            ))
    else:
        job_form = JobForm({'title': job.title, 'description': job.description,
            'category': job.category.id,
            'employment_type': job.employment_type,
            'employment_level': job.employment_level,
            'employer': job.employer.id,
        })
        job_form.fields['employer'].queryset = job_form.fields['employer'].queryset.filter(administrator=request.user)
        
        location_form = LocationForm({'address': job.location.address,
            'city': job.location.city,
            'state': job.location.state,
            'zip': job.location.zip,
        })
        contact_form = ContactForm({'name': job.contact.name,
            'email': job.contact.email,
            'phone': job.contact.phone,
            'fax': job.contact.fax,
            'url': job.contact.url,
        })
        
    return render_to_response(template_name, {
            'job_form': job_form,
            'location_form': location_form,
            'contact_form': contact_form,
            'add': False,
        }, context_instance=RequestContext(request)
    )
    
def create_employer(request, **kwargs):
    """
    employer creation 
    """
    template_name = kwargs.get("template_name", "djobs/employer_form.html")
    
    if request.method == 'POST':
        employer_form = EmployerForm(request.POST, request.FILES)
        
        if employer_form.is_valid():
            employer_name = employer_form.cleaned_data['name']
            profile = employer_form.cleaned_data['profile']
            logo = employer_form.cleaned_data['logo']
        
            new_employer_logo = EmployerLogo.objects.create(
                name="%s's logo" % employer_name,
                original_image=logo,
                caption="%s's logo" % employer_name,
            )
        
            new_employer = Employer.objects.create(
                name=employer_name,
                slug=slugify(employer_name),
                logo=new_employer_logo,
                profile=profile,
                administrator=request.user
            )
            
            return HttpResponseRedirect(reverse('djobs_edit_employer',
                args=[new_employer.id]
            ))
    else:
        employer_form = EmployerForm()
    
    return render_to_response(template_name, {
        'employer_form': employer_form,
        'add': True,
        }, context_instance=RequestContext(request)
    )
    
def edit_employer(request, employer_id, **kwargs):
    """
    employer editing/updating
    """
    template_name = kwargs.get("template_name", "djobs/employer_form.html")
    employer = get_object_or_404(Employer, pk=employer_id)
    
    if request.user != employer.administrator:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        employer_form = EmployerForm(request.POST)

        if employer_form.is_valid():
            employer.name = employer_form.cleaned_data['name']
            employer.profile = employer_form.cleaned_data['profile']
            
            if employer_form.cleaned_data['logo']:
                employer.logo = employer_form.cleaned_data['logo']
            elif employer.logo:
                employer.logo = employer.logo
                  
            employer.save()
            
            return HttpResponseRedirect(reverse('djobs_edit_employer',
                args=[employer.id]
            ))
    else:
        employer_form = EmployerForm({'name': employer.name, 
            'profile': employer.profile,
            'logo': employer.logo,
        })
       
    return render_to_response(template_name, {
            'employer_form': employer_form,
            'add': False,
        }, context_instance=RequestContext(request)
    )