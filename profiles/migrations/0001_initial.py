# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'profiles_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'profiles', ['Profile'])

        # Adding M2M table for field r_patrimony on 'Profile'
        db.create_table(u'profiles_profile_r_patrimony', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'profiles.profile'], null=False)),
            ('building', models.ForeignKey(orm[u'geodata.building'], null=False))
        ))
        db.create_unique(u'profiles_profile_r_patrimony', ['profile_id', 'building_id'])

        # Adding M2M table for field r_construction on 'Profile'
        db.create_table(u'profiles_profile_r_construction', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'profiles.profile'], null=False)),
            ('worksite', models.ForeignKey(orm[u'geodata.worksite'], null=False))
        ))
        db.create_unique(u'profiles_profile_r_construction', ['profile_id', 'worksite_id'])

        # Adding M2M table for field r_meeting on 'Profile'
        db.create_table(u'profiles_profile_r_meeting', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'profiles.profile'], null=False)),
            ('event', models.ForeignKey(orm[u'geodata.event'], null=False))
        ))
        db.create_unique(u'profiles_profile_r_meeting', ['profile_id', 'event_id'])

        # Adding M2M table for field r_actor on 'Profile'
        db.create_table(u'profiles_profile_r_actor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'profiles.profile'], null=False)),
            ('stakeholder', models.ForeignKey(orm[u'geodata.stakeholder'], null=False))
        ))
        db.create_unique(u'profiles_profile_r_actor', ['profile_id', 'stakeholder_id'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'profiles_profile')

        # Removing M2M table for field r_patrimony on 'Profile'
        db.delete_table('profiles_profile_r_patrimony')

        # Removing M2M table for field r_construction on 'Profile'
        db.delete_table('profiles_profile_r_construction')

        # Removing M2M table for field r_meeting on 'Profile'
        db.delete_table('profiles_profile_r_meeting')

        # Removing M2M table for field r_actor on 'Profile'
        db.delete_table('profiles_profile_r_actor')


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
            'ident_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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
            'ident_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'geodata.image': {
            'Meta': {'ordering': "['id']", 'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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
        },
        u'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_actor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Stakeholder']", 'null': 'True', 'blank': 'True'}),
            'r_construction': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Worksite']", 'null': 'True', 'blank': 'True'}),
            'r_meeting': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Event']", 'null': 'True', 'blank': 'True'}),
            'r_patrimony': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['geodata.Building']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['profiles']