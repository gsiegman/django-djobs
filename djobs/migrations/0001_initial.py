# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('djobs_location', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('djobs', ['Location'])

        # Adding model 'Contact'
        db.create_table('djobs_contact', (
            ('fax', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('djobs', ['Contact'])

        # Adding model 'EmployerLogo'
        db.create_table('djobs_employerlogo', (
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('djobs', ['EmployerLogo'])

        # Adding model 'Employer'
        db.create_table('djobs_employer', (
            ('profile', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('administrator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djobs.EmployerLogo'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('djobs', ['Employer'])

        # Adding model 'JobCategory'
        db.create_table('djobs_jobcategory', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('djobs', ['JobCategory'])

        # Adding model 'Job'
        db.create_table('djobs_job', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', to=orm['djobs.JobCategory'])),
            ('allow_applications', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('employment_type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('employment_level', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', to=orm['djobs.Employer'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djobs.Contact'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djobs.Location'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('djobs', ['Job'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('djobs_location')

        # Deleting model 'Contact'
        db.delete_table('djobs_contact')

        # Deleting model 'EmployerLogo'
        db.delete_table('djobs_employerlogo')

        # Deleting model 'Employer'
        db.delete_table('djobs_employer')

        # Deleting model 'JobCategory'
        db.delete_table('djobs_jobcategory')

        # Deleting model 'Job'
        db.delete_table('djobs_job')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djobs.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'djobs.employer': {
            'Meta': {'object_name': 'Employer'},
            'administrator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobs.EmployerLogo']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'profile': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'djobs.employerlogo': {
            'Meta': {'object_name': 'EmployerLogo'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'djobs.job': {
            'Meta': {'object_name': 'Job'},
            'allow_applications': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['djobs.JobCategory']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobs.Contact']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['djobs.Employer']"}),
            'employment_level': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'employment_type': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobs.Location']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'djobs.jobcategory': {
            'Meta': {'object_name': 'JobCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'djobs.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }
    
    complete_apps = ['djobs']
