from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import F

import datetime

EMPLOYMENT_TYPE_CHOICES = (
    ('ft', 'Full Time'),
    ('pt', 'Part Time'),
    ('temp', 'Temporary/Contract'),
    ('seas', 'Seasonal'),
    ('int', 'Internship'),
    ('free', 'Freelance'),
)

EMPLOYMENT_LEVEL_CHOICES = (
    ('ent', 'Entry'),
    ('ass', 'Assistant'),
    ('exp', 'Experienced/Specialist'),
    ('man', 'Management'),
    ('exec', 'Executive/Senior Management'),
)

class Location(models.Model):
    address = models.CharField(_('address'), max_length=200, blank=True, help_text=_("Max 200 chars. Not required."))
    city = models.CharField(_('city'), max_length=100, help_text=_("Max 100 chars. Required."))
    state = models.CharField(_('state'), max_length=2, choices=STATE_CHOICES, help_text=_("Required."))
    zip = models.CharField(_('zip'), max_length=5, help_text=_("5 digit zip code. Required."))
    
    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        
    def __unicode__(self):
        return '%s \n %s, %s %s' % (self.address, self.city, self.state, self.zip)
    
class Contact(models.Model):
    name = models.CharField(_('name'), max_length=100, help_text=_('Required.'))
    email = models.EmailField(_('email'), help_text=_('Required.'))
    phone = PhoneNumberField(_('phone'), blank=True, help_text=_('Not required.'))
    fax = PhoneNumberField(_('fax'), blank=True, help_text=_('Not required.'))
    url = models.URLField(_('url'), blank=True, help_text=_('Not required.'))
    
    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        
    def __unicode__(self):
        return self.name

class Employer(models.Model):
    name = models.CharField(_('name'), max_length=50, help_text=_("Max 50 chars. Required."))
    slug = models.SlugField(_('slug'), help_text=_("Only letters, numbers, or hyphens. Required."))
    logo = models.ImageField(_('logo'), upload_to='djobs/employer_logos')
    profile = models.TextField(_('profile'), blank=True)
    administrator = models.ForeignKey(User)
    
    class Meta:
        verbose_name = _('employer')
        verbose_name_plural = _('employers')
        
    def __unicode__(self):
        return self.name

class JobCategory(models.Model):
    title = models.CharField(_('title'), max_length=50, help_text=_("Max 50 chars. Required."))
    slug = models.SlugField(_('slug'), help_text=_("Only letters, numbers, or hyphens. Required."))
    
    class Meta:
        verbose_name = _('job category')
        verbose_name_plural = _('job categories')
        
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('djobs_category_jobs', args=[self.slug])
    
    @property
    def active_job_count(self):
        return len(Job.active.filter(category=self))

class ActiveJobManager(models.Manager):
    def get_query_set(self):
        return super(ActiveJobManager, self).get_query_set().filter(created_date__gte=datetime.datetime.now() - datetime.timedelta(days=30))

class Job(models.Model):
    title = models.CharField(_('title'), max_length=50, help_text=_("Max 50 chars. Required."))
    description = models.TextField(_('description'), help_text=_("Required."))
    category = models.ForeignKey(JobCategory, related_name='jobs')
    employment_type = models.CharField(_('employment type'), max_length=5, choices=EMPLOYMENT_TYPE_CHOICES, help_text=_("Required."))
    employment_level = models.CharField(_('employment level'), max_length=5, choices=EMPLOYMENT_LEVEL_CHOICES, help_text=_("Required."))
    employer = models.ForeignKey(Employer)
    location = models.ForeignKey(Location)
    contact = models.ForeignKey(Contact)
    allow_applications = models.BooleanField(_('allow applications'))
    created_date = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    active = ActiveJobManager()
    
    class Meta:
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        
    def __unicode__(self):
        return '%s at %s' % (self.title, self.employer.name)
