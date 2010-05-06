from django.conf.urls.defaults import *

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