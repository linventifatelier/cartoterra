# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EarthTechnique'
        db.create_table(u'geodata_earthtechnique', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'geodata', ['EarthTechnique'])

        # Adding model 'Image'
        db.create_table(u'geodata_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('legend', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'geodata', ['Image'])

        # Adding model 'EarthRoleTranslation'
        db.create_table(u'geodata_earthrole_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['geodata.EarthRole'])),
        ))
        db.send_create_signal(u'geodata', ['EarthRoleTranslation'])

        # Adding unique constraint on 'EarthRoleTranslation', fields ['language_code', 'master']
        db.create_unique(u'geodata_earthrole_translation', ['language_code', 'master_id'])

        # Adding model 'EarthRole'
        db.create_table(u'geodata_earthrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'geodata', ['EarthRole'])

        # Adding model 'Stakeholder'
        db.create_table(u'geodata_stakeholder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 2, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geodata', ['Stakeholder'])

        # Adding M2M table for field role on 'Stakeholder'
        db.create_table(u'geodata_stakeholder_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stakeholder', models.ForeignKey(orm[u'geodata.stakeholder'], null=False)),
            ('earthrole', models.ForeignKey(orm[u'geodata.earthrole'], null=False))
        ))
        db.create_unique(u'geodata_stakeholder_role', ['stakeholder_id', 'earthrole_id'])

        # Adding model 'Building'
        db.create_table(u'geodata_building', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 2, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('architects', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('unesco', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inauguration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geodata', ['Building'])

        # Adding M2M table for field techniques on 'Building'
        db.create_table(u'geodata_building_techniques', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm[u'geodata.building'], null=False)),
            ('earthtechnique', models.ForeignKey(orm[u'geodata.earthtechnique'], null=False))
        ))
        db.create_unique(u'geodata_building_techniques', ['building_id', 'earthtechnique_id'])

        # Adding M2M table for field stakeholder on 'Building'
        db.create_table(u'geodata_building_stakeholder', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm[u'geodata.building'], null=False)),
            ('stakeholder', models.ForeignKey(orm[u'geodata.stakeholder'], null=False))
        ))
        db.create_unique(u'geodata_building_stakeholder', ['building_id', 'stakeholder_id'])

        # Adding model 'EventTypeTranslation'
        db.create_table(u'geodata_eventtype_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['geodata.EventType'])),
        ))
        db.send_create_signal(u'geodata', ['EventTypeTranslation'])

        # Adding unique constraint on 'EventTypeTranslation', fields ['language_code', 'master']
        db.create_unique(u'geodata_eventtype_translation', ['language_code', 'master_id'])

        # Adding model 'EventType'
        db.create_table(u'geodata_eventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'geodata', ['EventType'])

        # Adding model 'Worksite'
        db.create_table(u'geodata_worksite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 2, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('participative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inauguration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geodata', ['Worksite'])

        # Adding M2M table for field techniques on 'Worksite'
        db.create_table(u'geodata_worksite_techniques', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('worksite', models.ForeignKey(orm[u'geodata.worksite'], null=False)),
            ('earthtechnique', models.ForeignKey(orm[u'geodata.earthtechnique'], null=False))
        ))
        db.create_unique(u'geodata_worksite_techniques', ['worksite_id', 'earthtechnique_id'])

        # Adding M2M table for field stakeholder on 'Worksite'
        db.create_table(u'geodata_worksite_stakeholder', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('worksite', models.ForeignKey(orm[u'geodata.worksite'], null=False)),
            ('stakeholder', models.ForeignKey(orm[u'geodata.stakeholder'], null=False))
        ))
        db.create_unique(u'geodata_worksite_stakeholder', ['worksite_id', 'stakeholder_id'])

        # Adding model 'Event'
        db.create_table(u'geodata_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 2, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geodata.EventType'], null=True, blank=True)),
            ('beginning_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 4, 2, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 4, 2, 0, 0))),
        ))
        db.send_create_signal(u'geodata', ['Event'])

        # Adding M2M table for field stakeholder on 'Event'
        db.create_table(u'geodata_event_stakeholder', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'geodata.event'], null=False)),
            ('stakeholder', models.ForeignKey(orm[u'geodata.stakeholder'], null=False))
        ))
        db.create_unique(u'geodata_event_stakeholder', ['event_id', 'stakeholder_id'])

        # Adding model 'Profile'
        db.create_table(u'geodata_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'geodata', ['Profile'])

        # Adding M2M table for field r_building on 'Profile'
        db.create_table(u'geodata_profile_r_building', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'geodata.profile'], null=False)),
            ('building', models.ForeignKey(orm[u'geodata.building'], null=False))
        ))
        db.create_unique(u'geodata_profile_r_building', ['profile_id', 'building_id'])

        # Adding M2M table for field r_worksite on 'Profile'
        db.create_table(u'geodata_profile_r_worksite', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'geodata.profile'], null=False)),
            ('worksite', models.ForeignKey(orm[u'geodata.worksite'], null=False))
        ))
        db.create_unique(u'geodata_profile_r_worksite', ['profile_id', 'worksite_id'])

        # Adding M2M table for field r_event on 'Profile'
        db.create_table(u'geodata_profile_r_event', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'geodata.profile'], null=False)),
            ('event', models.ForeignKey(orm[u'geodata.event'], null=False))
        ))
        db.create_unique(u'geodata_profile_r_event', ['profile_id', 'event_id'])

        # Adding M2M table for field r_stakeholder on 'Profile'
        db.create_table(u'geodata_profile_r_stakeholder', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'geodata.profile'], null=False)),
            ('stakeholder', models.ForeignKey(orm[u'geodata.stakeholder'], null=False))
        ))
        db.create_unique(u'geodata_profile_r_stakeholder', ['profile_id', 'stakeholder_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'EventTypeTranslation', fields ['language_code', 'master']
        db.delete_unique(u'geodata_eventtype_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'EarthRoleTranslation', fields ['language_code', 'master']
        db.delete_unique(u'geodata_earthrole_translation', ['language_code', 'master_id'])

        # Deleting model 'EarthTechnique'
        db.delete_table(u'geodata_earthtechnique')

        # Deleting model 'Image'
        db.delete_table(u'geodata_image')

        # Deleting model 'EarthRoleTranslation'
        db.delete_table(u'geodata_earthrole_translation')

        # Deleting model 'EarthRole'
        db.delete_table(u'geodata_earthrole')

        # Deleting model 'Stakeholder'
        db.delete_table(u'geodata_stakeholder')

        # Removing M2M table for field role on 'Stakeholder'
        db.delete_table('geodata_stakeholder_role')

        # Deleting model 'Building'
        db.delete_table(u'geodata_building')

        # Removing M2M table for field techniques on 'Building'
        db.delete_table('geodata_building_techniques')

        # Removing M2M table for field stakeholder on 'Building'
        db.delete_table('geodata_building_stakeholder')

        # Deleting model 'EventTypeTranslation'
        db.delete_table(u'geodata_eventtype_translation')

        # Deleting model 'EventType'
        db.delete_table(u'geodata_eventtype')

        # Deleting model 'Worksite'
        db.delete_table(u'geodata_worksite')

        # Removing M2M table for field techniques on 'Worksite'
        db.delete_table('geodata_worksite_techniques')

        # Removing M2M table for field stakeholder on 'Worksite'
        db.delete_table('geodata_worksite_stakeholder')

        # Deleting model 'Event'
        db.delete_table(u'geodata_event')

        # Removing M2M table for field stakeholder on 'Event'
        db.delete_table('geodata_event_stakeholder')

        # Deleting model 'Profile'
        db.delete_table(u'geodata_profile')

        # Removing M2M table for field r_building on 'Profile'
        db.delete_table('geodata_profile_r_building')

        # Removing M2M table for field r_worksite on 'Profile'
        db.delete_table('geodata_profile_r_worksite')

        # Removing M2M table for field r_event on 'Profile'
        db.delete_table('geodata_profile_r_event')

        # Removing M2M table for field r_stakeholder on 'Profile'
        db.delete_table('geodata_profile_r_stakeholder')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'geodata.building': {
            'Meta': {'object_name': 'Building'},
            'architects': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inauguration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 2, 0, 0)'}),
            'stakeholder': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Stakeholder']", 'null': 'True', 'blank': 'True'}),
            'techniques': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.EarthTechnique']", 'null': 'True', 'blank': 'True'}),
            'unesco': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'geodata.earthrole': {
            'Meta': {'object_name': 'EarthRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'geodata.earthroletranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'EarthRoleTranslation', 'db_table': "u'geodata_earthrole_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['geodata.EarthRole']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'geodata.earthtechnique': {
            'Meta': {'object_name': 'EarthTechnique'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'geodata.event': {
            'Meta': {'object_name': 'Event'},
            'beginning_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 4, 2, 0, 0)'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 4, 2, 0, 0)'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geodata.EventType']", 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 2, 0, 0)'}),
            'stakeholder': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Stakeholder']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'geodata.eventtype': {
            'Meta': {'object_name': 'EventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'geodata.eventtypetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'EventTypeTranslation', 'db_table': "u'geodata_eventtype_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['geodata.EventType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'geodata.image': {
            'Meta': {'ordering': "['id']", 'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'geodata.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_building': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Building']", 'null': 'True', 'blank': 'True'}),
            'r_event': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Event']", 'null': 'True', 'blank': 'True'}),
            'r_stakeholder': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Stakeholder']", 'null': 'True', 'blank': 'True'}),
            'r_worksite': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Worksite']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'geodata.stakeholder': {
            'Meta': {'object_name': 'Stakeholder'},
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 2, 0, 0)'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.EarthRole']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'geodata.worksite': {
            'Meta': {'object_name': 'Worksite'},
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inauguration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'participative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 2, 0, 0)'}),
            'stakeholder': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Stakeholder']", 'null': 'True', 'blank': 'True'}),
            'techniques': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.EarthTechnique']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geodata']