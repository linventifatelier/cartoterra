# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
                ('contact', models.TextField(null=True, verbose_name='contact', blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('credit_creator', models.BooleanField(default=True, verbose_name='credit creator')),
                ('architects', models.TextField(null=True, verbose_name='architects', blank=True)),
                ('unesco', models.BooleanField(default=False, verbose_name='world heritage')),
                ('inauguration_date', models.DateField(null=True, verbose_name='inauguration date', blank=True)),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'building',
                'verbose_name_plural': 'buildings',
            },
        ),
        migrations.CreateModel(
            name='EarthRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident_name', models.CharField(unique=True, max_length=50, verbose_name='Identification name', validators=[django.core.validators.RegexValidator(regex=re.compile(b'^[a-zA-Z0-9_\\-]+$'))])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EarthRoleTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Translated name', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='geodata.EarthRole', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'geodata_earthrole_translation',
                'db_tablespace': '',
            },
        ),
        migrations.CreateModel(
            name='EarthTechnique',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
                ('contact', models.TextField(null=True, verbose_name='contact', blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('credit_creator', models.BooleanField(default=True, verbose_name='credit creator')),
                ('unesco_chair', models.BooleanField(default=False, verbose_name='UNESCO Chair Earthen Architecture')),
                ('beginning_date', models.DateField(default=None, verbose_name='beginning date')),
                ('end_date', models.DateField(default=None, verbose_name='end date')),
                ('number_of_stakeholders', models.PositiveIntegerField(null=True, verbose_name='Number of stakeholders', blank=True)),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident_name', models.CharField(unique=True, max_length=50, verbose_name='Identification name', validators=[django.core.validators.RegexValidator(regex=re.compile(b'^[a-zA-Z0-9_\\-]+$'))])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventTypeTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Translated name', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='geodata.EventType', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'geodata_eventtype_translation',
                'db_tablespace': '',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.ImageField(upload_to=b'img/geodata')),
                ('legend', models.CharField(max_length=100, null=True, verbose_name='caption', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r_building', models.ManyToManyField(related_name='recommended_by', verbose_name='building recommendations', to='geodata.Building', blank=True)),
                ('r_event', models.ManyToManyField(related_name='recommended_by', verbose_name='event recommendations', to='geodata.Event', blank=True)),
            ],
            options={
                'permissions': (('world_heritage', 'Can modify world heritage properties'), ('unesco_chair', 'Can modify UNESCO Chair Earthen Architecture')),
            },
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
                ('contact', models.TextField(null=True, verbose_name='contact', blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('unesco_chair', models.BooleanField(default=False, verbose_name='UNESCO Chair Earthen Architecture')),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
                ('role', models.ManyToManyField(to='geodata.EarthRole', verbose_name='role', blank=True)),
            ],
            options={
                'verbose_name': 'stakeholder',
            },
        ),
        migrations.CreateModel(
            name='Worksite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
                ('contact', models.TextField(null=True, verbose_name='contact', blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('credit_creator', models.BooleanField(default=True, verbose_name='credit creator')),
                ('participative', models.BooleanField(default=False, verbose_name='participative')),
                ('inauguration_date', models.DateField(verbose_name='inauguration date', blank=True)),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
                ('stakeholder', models.ManyToManyField(to='geodata.Stakeholder', verbose_name='stakeholder', blank=True)),
                ('techniques', models.ManyToManyField(to='geodata.EarthTechnique', verbose_name='techniques', blank=True)),
            ],
            options={
                'verbose_name': 'worksite',
                'verbose_name_plural': 'worksites',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='r_stakeholder',
            field=models.ManyToManyField(related_name='recommended_by', verbose_name='stakeholder recommendations', to='geodata.Stakeholder', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='r_worksite',
            field=models.ManyToManyField(related_name='recommended_by', verbose_name='worksite recommendations', to='geodata.Worksite', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(verbose_name='event type', blank=True, to='geodata.EventType', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='stakeholder',
            field=models.ManyToManyField(to='geodata.Stakeholder', verbose_name='stakeholder', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='type_of_stakeholders',
            field=models.ManyToManyField(to='geodata.EarthRole', verbose_name='Type of stakeholders', blank=True),
        ),
        migrations.AddField(
            model_name='building',
            name='stakeholder',
            field=models.ManyToManyField(to='geodata.Stakeholder', verbose_name='stakeholder', blank=True),
        ),
        migrations.AddField(
            model_name='building',
            name='techniques',
            field=models.ManyToManyField(to='geodata.EarthTechnique', verbose_name='techniques', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='eventtypetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='earthroletranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
