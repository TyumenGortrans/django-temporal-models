# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PersonTemporal'
        db.create_table('app_person_temporal', (
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('salary', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('organization', self.gf('temporal.models.fields.TemporalForeignKey')(related_name='_temporal_person', to=orm['app.Organization'])),
            ('_temporal_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_temporal_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_temporal_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('app', ['PersonTemporal'])

        # Adding unique constraint on 'PersonTemporal', fields ['id', 'date_begin']
        db.create_unique('app_person_temporal', ['id', 'date_begin'])

        # Adding model 'Person'
        db.create_table('app_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('salary', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('organization', self.gf('temporal.models.fields.TemporalForeignKey')(to=orm['app.Organization'])),
        ))
        db.send_create_signal('app', ['Person'])

        # Adding unique constraint on 'Person', fields ['id', 'date_begin']
        db.create_unique('app_person', ['id', 'date_begin'])

        # Adding model 'OrganizationTemporal'
        db.create_table('app_organization_temporal', (
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_temporal_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_temporal_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_temporal_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('app', ['OrganizationTemporal'])

        # Adding unique constraint on 'OrganizationTemporal', fields ['id', 'date_begin']
        db.create_unique('app_organization_temporal', ['id', 'date_begin'])

        # Adding model 'Organization'
        db.create_table('app_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('app', ['Organization'])

        # Adding unique constraint on 'Organization', fields ['id', 'date_begin']
        db.create_unique('app_organization', ['id', 'date_begin'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Organization', fields ['id', 'date_begin']
        db.delete_unique('app_organization', ['id', 'date_begin'])

        # Removing unique constraint on 'OrganizationTemporal', fields ['id', 'date_begin']
        db.delete_unique('app_organization_temporal', ['id', 'date_begin'])

        # Removing unique constraint on 'Person', fields ['id', 'date_begin']
        db.delete_unique('app_person', ['id', 'date_begin'])

        # Removing unique constraint on 'PersonTemporal', fields ['id', 'date_begin']
        db.delete_unique('app_person_temporal', ['id', 'date_begin'])

        # Deleting model 'PersonTemporal'
        db.delete_table('app_person_temporal')

        # Deleting model 'Person'
        db.delete_table('app_person')

        # Deleting model 'OrganizationTemporal'
        db.delete_table('app_organization_temporal')

        # Deleting model 'Organization'
        db.delete_table('app_organization')


    models = {
        'app.organization': {
            'Meta': {'unique_together': "(('id', 'date_begin'),)", 'object_name': 'Organization'},
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'app.organizationtemporal': {
            'Meta': {'ordering': "['-_temporal_timestamp']", 'unique_together': "(('id', 'date_begin'),)", 'object_name': 'OrganizationTemporal', 'db_table': "'app_organization_temporal'"},
            '_temporal_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_temporal_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_temporal_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'app.person': {
            'Meta': {'unique_together': "(('id', 'date_begin'),)", 'object_name': 'Person'},
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('temporal.models.fields.TemporalForeignKey', [], {'to': "orm['app.Organization']"}),
            'salary': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'app.persontemporal': {
            'Meta': {'ordering': "['-_temporal_timestamp']", 'unique_together': "(('id', 'date_begin'),)", 'object_name': 'PersonTemporal', 'db_table': "'app_person_temporal'"},
            '_temporal_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_temporal_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_temporal_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('temporal.models.fields.TemporalForeignKey', [], {'related_name': "'_temporal_person'", 'to': "orm['app.Organization']"}),
            'salary': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['app']
