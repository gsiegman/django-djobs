from django import template
from django.db.models import Count
from djobs.models import JobCategory, Job

register = template.Library()

def job_categories():
    categories = JobCategory.objects.all()
    categories_with_jobs = []
    categories_no_jobs = []
    
    for category in categories:
        if category.active_job_count == 0:
            categories_no_jobs.append(category)
        else:
            categories_with_jobs.append(category)
    
    return {
        'categories': categories,
        'categories_with_jobs': categories_with_jobs,
        'categories_no_jobs': categories_no_jobs,
    }

register.inclusion_tag('djobs/categories.html')(job_categories)

class RecentJobsNode(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name
        
    def render(self, context):
        jobs = Job.active.all()[:self.limit]
        context[self.var_name] = jobs
        return ''
        
@register.tag
def get_recent_jobs(parser, token):
    args = token.split_contents()
    limit = args[1]
    var_name = args[-1]
    return RecentJobsNode(limit, var_name)
    
register.tag()(get_recent_jobs)

class RecentJobsForObjNode(template.Node):
    def __init__(self, obj, limit, var_name):
        self.obj = template.Variable(obj)
        self.limit = limit
        self.var_name = var_name
        
    def render(self, context):
        jobs = self.obj.resolve(context).jobs.all()[:self.limit]
        context[self.var_name] = jobs
        return ''
        
@register.tag
def get_recent_jobs_for_obj(parser, token):
    args = token.split_contents()
    obj = args[1]
    limit = args[2]
    var_name = args[-1]
    return RecentJobsForObjNode(obj, limit, var_name)
    
register.tag()(get_recent_jobs_for_obj)