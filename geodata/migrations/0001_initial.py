# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EarthTechnique'
        db.create_table('geodata_earthtechnique', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('geodata', ['EarthTechnique'])

        # Adding model 'EarthRoleTranslation'
        db.create_table('geodata_earthrole_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['geodata.EarthRole'])),
        ))
        db.send_create_signal('geodata', ['EarthRoleTranslation'])

        # Adding unique constraint on 'EarthRoleTranslation', fields ['language_code', 'master']
        db.create_unique('geodata_earthrole_translation', ['language_code', 'master_id'])

        # Adding model 'EarthRole'
        db.create_table('geodata_earthrole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('geodata', ['EarthRole'])

        # Adding model 'EarthGeoDataActor'
        db.create_table('geodata_earthgeodataactor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 16, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('geodata', ['EarthGeoDataActor'])

        # Adding M2M table for field role on 'EarthGeoDataActor'
        db.create_table('geodata_earthgeodataactor_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodataactor', models.ForeignKey(orm['geodata.earthgeodataactor'], null=False)),
            ('earthrole', models.ForeignKey(orm['geodata.earthrole'], null=False))
        ))
        db.create_unique('geodata_earthgeodataactor_role', ['earthgeodataactor_id', 'earthrole_id'])

        # Adding model 'EarthGeoDataPatrimony'
        db.create_table('geodata_earthgeodatapatrimony', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 16, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('architects', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('unesco', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inauguration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('geodata', ['EarthGeoDataPatrimony'])

        # Adding M2M table for field techniques on 'EarthGeoDataPatrimony'
        db.create_table('geodata_earthgeodatapatrimony_techniques', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodatapatrimony', models.ForeignKey(orm['geodata.earthgeodatapatrimony'], null=False)),
            ('earthtechnique', models.ForeignKey(orm['geodata.earthtechnique'], null=False))
        ))
        db.create_unique('geodata_earthgeodatapatrimony_techniques', ['earthgeodatapatrimony_id', 'earthtechnique_id'])

        # Adding M2M table for field actor on 'EarthGeoDataPatrimony'
        db.create_table('geodata_earthgeodatapatrimony_actor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodatapatrimony', models.ForeignKey(orm['geodata.earthgeodatapatrimony'], null=False)),
            ('earthgeodataactor', models.ForeignKey(orm['geodata.earthgeodataactor'], null=False))
        ))
        db.create_unique('geodata_earthgeodatapatrimony_actor', ['earthgeodatapatrimony_id', 'earthgeodataactor_id'])

        # Adding model 'EarthMeetingTypeTranslation'
        db.create_table('geodata_earthmeetingtype_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['geodata.EarthMeetingType'])),
        ))
        db.send_create_signal('geodata', ['EarthMeetingTypeTranslation'])

        # Adding unique constraint on 'EarthMeetingTypeTranslation', fields ['language_code', 'master']
        db.create_unique('geodata_earthmeetingtype_translation', ['language_code', 'master_id'])

        # Adding model 'EarthMeetingType'
        db.create_table('geodata_earthmeetingtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('geodata', ['EarthMeetingType'])

        # Adding model 'EarthGeoDataMeeting'
        db.create_table('geodata_earthgeodatameeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 16, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('meeting_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geodata.EarthMeetingType'], null=True, blank=True)),
            ('beginning_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 16, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 16, 0, 0))),
        ))
        db.send_create_signal('geodata', ['EarthGeoDataMeeting'])

        # Adding M2M table for field actor on 'EarthGeoDataMeeting'
        db.create_table('geodata_earthgeodatameeting_actor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodatameeting', models.ForeignKey(orm['geodata.earthgeodatameeting'], null=False)),
            ('earthgeodataactor', models.ForeignKey(orm['geodata.earthgeodataactor'], null=False))
        ))
        db.create_unique('geodata_earthgeodatameeting_actor', ['earthgeodatameeting_id', 'earthgeodataactor_id'])

        # Adding model 'EarthGeoDataConstruction'
        db.create_table('geodata_earthgeodataconstruction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 16, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('participative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inauguration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('geodata', ['EarthGeoDataConstruction'])

        # Adding M2M table for field techniques on 'EarthGeoDataConstruction'
        db.create_table('geodata_earthgeodataconstruction_techniques', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodataconstruction', models.ForeignKey(orm['geodata.earthgeodataconstruction'], null=False)),
            ('earthtechnique', models.ForeignKey(orm['geodata.earthtechnique'], null=False))
        ))
        db.create_unique('geodata_earthgeodataconstruction_techniques', ['earthgeodataconstruction_id', 'earthtechnique_id'])

        # Adding M2M table for field actor on 'EarthGeoDataConstruction'
        db.create_table('geodata_earthgeodataconstruction_actor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodataconstruction', models.ForeignKey(orm['geodata.earthgeodataconstruction'], null=False)),
            ('earthgeodataactor', models.ForeignKey(orm['geodata.earthgeodataactor'], null=False))
        ))
        db.create_unique('geodata_earthgeodataconstruction_actor', ['earthgeodataconstruction_id', 'earthgeodataactor_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'EarthMeetingTypeTranslation', fields ['language_code', 'master']
        db.delete_unique('geodata_earthmeetingtype_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'EarthRoleTranslation', fields ['language_code', 'master']
        db.delete_unique('geodata_earthrole_translation', ['language_code', 'master_id'])

        # Deleting model 'EarthTechnique'
        db.delete_table('geodata_earthtechnique')

        # Deleting model 'EarthRoleTranslation'
        db.delete_table('geodata_earthrole_translation')

        # Deleting model 'EarthRole'
        db.delete_table('geodata_earthrole')

        # Deleting model 'EarthGeoDataActor'
        db.delete_table('geodata_earthgeodataactor')

        # Removing M2M table for field role on 'EarthGeoDataActor'
        db.delete_table('geodata_earthgeodataactor_role')

        # Deleting model 'EarthGeoDataPatrimony'
        db.delete_table('geodata_earthgeodatapatrimony')

        # Removing M2M table for field techniques on 'EarthGeoDataPatrimony'
        db.delete_table('geodata_earthgeodatapatrimony_techniques')

        # Removing M2M table for field actor on 'EarthGeoDataPatrimony'
        db.delete_table('geodata_earthgeodatapatrimony_actor')

        # Deleting model 'EarthMeetingTypeTranslation'
        db.delete_table('geodata_earthmeetingtype_translation')

        # Deleting model 'EarthMeetingType'
        db.delete_table('geodata_earthmeetingtype')

        # Deleting model 'EarthGeoDataMeeting'
        db.delete_table('geodata_earthgeodatameeting')

        # Removing M2M table for field actor on 'EarthGeoDataMeeting'
        db.delete_table('geodata_earthgeodatameeting_actor')

        # Deleting model 'EarthGeoDataConstruction'
        db.delete_table('geodata_earthgeodataconstruction')

        # Removing M2M table for field techniques on 'EarthGeoDataConstruction'
        db.delete_table('geodata_earthgeodataconstruction_techniques')

        # Removing M2M table for field actor on 'EarthGeoDataConstruction'
        db.delete_table('geodata_earthgeodataconstruction_actor')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geodata.earthgeodataactor': {
            'Meta': {'object_name': 'EarthGeoDataActor'},
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthRole']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthgeodataconstruction': {
            'Meta': {'object_name': 'EarthGeoDataConstruction'},
            'actor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthGeoDataActor']", 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'inauguration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'participative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)'}),
            'techniques': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthTechnique']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthgeodatameeting': {
            'Meta': {'object_name': 'EarthGeoDataMeeting'},
            'actor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthGeoDataActor']", 'null': 'True', 'blank': 'True'}),
            'beginning_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'meeting_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geodata.EarthMeetingType']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthgeodatapatrimony': {
            'Meta': {'object_name': 'EarthGeoDataPatrimony'},
            'actor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthGeoDataActor']", 'null': 'True', 'blank': 'True'}),
            'architects': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'inauguration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 16, 0, 0)'}),
            'techniques': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthTechnique']", 'null': 'True', 'blank': 'True'}),
            'unesco': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthmeetingtype': {
            'Meta': {'object_name': 'EarthMeetingType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'geodata.earthmeetingtypetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'EarthMeetingTypeTranslation', 'db_table': "'geodata_earthmeetingtype_translation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['geodata.EarthMeetingType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthrole': {
            'Meta': {'object_name': 'EarthRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'geodata.earthroletranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'EarthRoleTranslation', 'db_table': "'geodata_earthrole_translation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['geodata.EarthRole']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthtechnique': {
            'Meta': {'object_name': 'EarthTechnique'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geodata']