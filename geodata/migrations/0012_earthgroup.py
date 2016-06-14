# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0011_auto_20160601_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='EarthGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description_markdown', models.TextField(null=True, verbose_name='description', blank=True)),
                ('description', models.TextField(null=True, editable=False, blank=True)),
                ('logo', models.ImageField(upload_to=b'img/group')),
            ],
        ),
    ]
