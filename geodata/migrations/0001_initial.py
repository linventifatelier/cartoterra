# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BookTranslation'
        db.create_table('geodata_book_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['geodata.Book'])),
        ))
        db.send_create_signal('geodata', ['BookTranslation'])

        # Adding unique constraint on 'BookTranslation', fields ['language_code', 'master']
        db.create_unique('geodata_book_translation', ['language_code', 'master_id'])

        # Adding model 'Book'
        db.create_table('geodata_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=17)),
        ))
        db.send_create_signal('geodata', ['Book'])

        # Adding model 'EarthTechnique'
        db.create_table('geodata_earthtechnique', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('geodata', ['EarthTechnique'])

        # Adding model 'EarthArchitect'
        db.create_table('geodata_eartharchitect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('geodata', ['EarthArchitect'])

        # Adding model 'EarthGeoDataPatrimony'
        db.create_table('geodata_earthgeodatapatrimony', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 18, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('unesco', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inauguration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('geodata', ['EarthGeoDataPatrimony'])

        # Adding M2M table for field architects on 'EarthGeoDataPatrimony'
        db.create_table('geodata_earthgeodatapatrimony_architects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodatapatrimony', models.ForeignKey(orm['geodata.earthgeodatapatrimony'], null=False)),
            ('eartharchitect', models.ForeignKey(orm['geodata.eartharchitect'], null=False))
        ))
        db.create_unique('geodata_earthgeodatapatrimony_architects', ['earthgeodatapatrimony_id', 'eartharchitect_id'])

        # Adding M2M table for field techniques on 'EarthGeoDataPatrimony'
        db.create_table('geodata_earthgeodatapatrimony_techniques', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('earthgeodatapatrimony', models.ForeignKey(orm['geodata.earthgeodatapatrimony'], null=False)),
            ('earthtechnique', models.ForeignKey(orm['geodata.earthtechnique'], null=False))
        ))
        db.create_unique('geodata_earthgeodatapatrimony_techniques', ['earthgeodatapatrimony_id', 'earthtechnique_id'])

        # Adding model 'EarthGeoDataMeeting'
        db.create_table('geodata_earthgeodatameeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 18, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('meeting_type', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('beginning_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 9, 18, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 9, 18, 0, 0))),
        ))
        db.send_create_signal('geodata', ['EarthGeoDataMeeting'])

        # Adding model 'EarthGeoDataConstruction'
        db.create_table('geodata_earthgeodataconstruction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 18, 0, 0))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('credit_creator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
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


    def backwards(self, orm):
        # Removing unique constraint on 'BookTranslation', fields ['language_code', 'master']
        db.delete_unique('geodata_book_translation', ['language_code', 'master_id'])

        # Deleting model 'BookTranslation'
        db.delete_table('geodata_book_translation')

        # Deleting model 'Book'
        db.delete_table('geodata_book')

        # Deleting model 'EarthTechnique'
        db.delete_table('geodata_earthtechnique')

        # Deleting model 'EarthArchitect'
        db.delete_table('geodata_eartharchitect')

        # Deleting model 'EarthGeoDataPatrimony'
        db.delete_table('geodata_earthgeodatapatrimony')

        # Removing M2M table for field architects on 'EarthGeoDataPatrimony'
        db.delete_table('geodata_earthgeodatapatrimony_architects')

        # Removing M2M table for field techniques on 'EarthGeoDataPatrimony'
        db.delete_table('geodata_earthgeodatapatrimony_techniques')

        # Deleting model 'EarthGeoDataMeeting'
        db.delete_table('geodata_earthgeodatameeting')

        # Deleting model 'EarthGeoDataConstruction'
        db.delete_table('geodata_earthgeodataconstruction')

        # Removing M2M table for field techniques on 'EarthGeoDataConstruction'
        db.delete_table('geodata_earthgeodataconstruction_techniques')


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
        'geodata.book': {
            'Meta': {'object_name': 'Book'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '17'})
        },
        'geodata.booktranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'BookTranslation', 'db_table': "'geodata_book_translation'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['geodata.Book']"})
        },
        'geodata.eartharchitect': {
            'Meta': {'object_name': 'EarthArchitect'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthgeodataconstruction': {
            'Meta': {'object_name': 'EarthGeoDataConstruction'},
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'inauguration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'participative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)'}),
            'techniques': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthTechnique']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthgeodatameeting': {
            'Meta': {'object_name': 'EarthGeoDataMeeting'},
            'beginning_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'meeting_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'geodata.earthgeodatapatrimony': {
            'Meta': {'object_name': 'EarthGeoDataPatrimony'},
            'architects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthArchitect']", 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'credit_creator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'inauguration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)'}),
            'techniques': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geodata.EarthTechnique']", 'null': 'True', 'blank': 'True'}),
            'unesco': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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