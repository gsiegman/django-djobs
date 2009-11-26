from django.contrib import admin
from djobs.models import Contact, Employer, Job, JobCategory, Location

admin.site.register(Employer)

admin.site.register(Job)

class JobCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }

admin.site.register(JobCategory, JobCategoryAdmin)

admin.site.register(Location)

admin.site.register(Contact)