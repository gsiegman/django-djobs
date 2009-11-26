from django import template
from django.db.models import Count
from djobs.models import JobCategory

register = template.Library()

def job_categories():
    categories = JobCategory.objects.all()
    return {'categories': categories}

register.inclusion_tag('djobs/categories.html')(job_categories)