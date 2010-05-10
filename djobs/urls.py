from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from djobs.views import create_job, edit_job, \
    create_employer, edit_employer

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 
        'direct_to_template', 
        {'template': 'djobs/index.html'}, 
        name='djobs_index_view'
    ),
)

urlpatterns += patterns('djobs.views',
    url(r'^categories/(?P<slug>[-\w]+)/$', 
        'category_jobs', 
        name='djobs_category_jobs'
    ),
    url(r'^employers/(?P<id>\d+)/$', 
        'employer_jobs', 
        name='djobs_employer_jobs'
    ),
    url(r'^jobs/(?P<id>\d+)/$', 
        'job_detail', 
        name='djobs_job_detail'
    ),   
)

urlpatterns += patterns('',
    url(r'^jobs/create/$',
        login_required(create_job),
        name='djobs_create_job'
    ),
    url(r'^jobs/edit/(?P<job_id>\d+)/$',
        login_required(edit_job),
        name='djobs_edit_job'
    ),
    url(r'^employers/create/$',
        login_required(create_employer),
        name='djobs_create_employer'
    ),
    url(r'^employers/edit/(?P<employer_id>\d+)/$',
        login_required(edit_employer),
        name='djobs_edit_employer'
    ),
)