from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from djobs.views import create_job, edit_job, delete_job, \
    create_employer, edit_employer, manage

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
        'employer_detail', 
        name='djobs_employer_detail'
    ),
    url(r'^jobs/(?P<id>\d+)/$', 
        'job_detail', 
        name='djobs_job_detail'
    ),
    url(r'^search/$',
        'search',
        name='djobs_search',
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
    url(r'^jobs/delete/(?P<job_id>\d+)/$',
        login_required(delete_job),
        name='djobs_delete_job'
    ),
    url(r'^employers/create/$',
        login_required(create_employer),
        name='djobs_create_employer'
    ),
    url(r'^employers/edit/(?P<employer_id>\d+)/$',
        login_required(edit_employer),
        name='djobs_edit_employer'
    ),
    url(r'^manage/$',
        login_required(manage),
        name='djobs_manage',
    ),
)