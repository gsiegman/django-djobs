from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response

from djobs.models import Job, JobCategory
import datetime

def category_jobs(request, slug):
    category = JobCategory.objects.get(slug=slug)
    jobs = Job.active.filter(category=category)
    
    return object_list(request, 
        queryset=jobs, 
        allow_empty=True, 
        template_name='djobs/category_jobs.html', 
        extra_context={'category': category}
    )
    
def job_detail(request, id):
    jobs = Job.active.all()
    
    return object_detail(request, 
        queryset=jobs, 
        object_id=id, 
        template_name='djobs/job_detail.html')