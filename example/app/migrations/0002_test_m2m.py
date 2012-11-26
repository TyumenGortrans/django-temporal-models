# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GroupTemporal'
        db.create_table('app_group_temporal', (
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_temporal_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_temporal_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_temporal_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('app', ['GroupTemporal'])

        # Adding unique constraint on 'GroupTemporal', fields ['id', 'date_begin']
        db.create_unique('app_group_temporal', ['id', 'date_begin'])

        # Adding model 'PersonGroupTemporal'
        db.create_table('app_persongroup_temporal', (
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('person', self.gf('temporal.models.fields.TemporalForeignKey')(related_name='_temporal_persongroup', to=orm['app.Person'])),
            ('group', self.gf('temporal.models.fields.TemporalForeignKey')(related_name='_temporal_persongroup', to=orm['app.Group'])),
            ('_temporal_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_temporal_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_temporal_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('app', ['PersonGroupTemporal'])

        # Adding unique constraint on 'PersonGroupTemporal', fields ['person', 'group', 'date_begin']
        db.create_unique('app_persongroup_temporal', ['person_id', 'group_id', 'date_begin'])

        # Adding model 'PersonGroup'
        db.create_table('app_persongroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('person', self.gf('temporal.models.fields.TemporalForeignKey')(to=orm['app.Person'])),
            ('group', self.gf('temporal.models.fields.TemporalForeignKey')(to=orm['app.Group'])),
        ))
        db.send_create_signal('app', ['PersonGroup'])

        # Adding unique constraint on 'PersonGroup', fields ['person', 'group', 'date_begin']
        db.create_unique('app_persongroup', ['person_id', 'group_id', 'date_begin'])

        # Adding model 'Group'
        db.create_table('app_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('app', ['Group'])

        # Adding unique constraint on 'Group', fields ['id', 'date_begin']
        db.create_unique('app_group', ['id', 'date_begin'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Group', fields ['id', 'date_begin']
        db.delete_unique('app_group', ['id', 'date_begin'])

        # Removing unique constraint on 'PersonGroup', fields ['person', 'group', 'date_begin']
        db.delete_unique('app_persongroup', ['person_id', 'group_id', 'date_begin'])

        # Removing unique constraint on 'PersonGroupTemporal', fields ['person', 'group', 'date_begin']
        db.delete_unique('app_persongroup_temporal', ['person_id', 'group_id', 'date_begin'])

        # Removing unique constraint on 'GroupTemporal', fields ['id', 'date_begin']
        db.delete_unique('app_group_temporal', ['id', 'date_begin'])

        # Deleting model 'GroupTemporal'
        db.delete_table('app_group_temporal')

        # Deleting model 'PersonGroupTemporal'
        db.delete_table('app_persongroup_temporal')

        # Deleting model 'PersonGroup'
        db.delete_table('app_persongroup')

        # Deleting model 'Group'
        db.delete_table('app_group')


    models = {
        'app.group': {
            'Meta': {'unique_together': "(('id', 'date_begin'),)", 'object_name': 'Group'},
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'app.grouptemporal': {
            'Meta': {'ordering': "['-_temporal_timestamp']", 'unique_together': "(('id', 'date_begin'),)", 'object_name': 'GroupTemporal', 'db_table': "'app_group_temporal'"},
            '_temporal_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_temporal_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_temporal_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Group']", 'through': "orm['app.PersonGroup']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('temporal.models.fields.TemporalForeignKey', [], {'to': "orm['app.Organization']"}),
            'salary': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'app.persongroup': {
            'Meta': {'unique_together': "(('person', 'group', 'date_begin'),)", 'object_name': 'PersonGroup'},
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('temporal.models.fields.TemporalForeignKey', [], {'to': "orm['app.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('temporal.models.fields.TemporalForeignKey', [], {'to': "orm['app.Person']"})
        },
        'app.persongrouptemporal': {
            'Meta': {'ordering': "['-_temporal_timestamp']", 'unique_together': "(('person', 'group', 'date_begin'),)", 'object_name': 'PersonGroupTemporal', 'db_table': "'app_persongroup_temporal'"},
            '_temporal_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_temporal_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_temporal_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('temporal.models.fields.TemporalForeignKey', [], {'related_name': "'_temporal_persongroup'", 'to': "orm['app.Group']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'person': ('temporal.models.fields.TemporalForeignKey', [], {'related_name': "'_temporal_persongroup'", 'to': "orm['app.Person']"})
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
