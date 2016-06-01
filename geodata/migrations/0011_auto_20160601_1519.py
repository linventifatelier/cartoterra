# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0010_auto_20151217_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='techniques',
            field=models.ManyToManyField(to='geodata.EarthTechnique', verbose_name='techniques', blank=True),
        ),
        migrations.AddField(
            model_name='stakeholder',
            name='techniques',
            field=models.ManyToManyField(to='geodata.EarthTechnique', verbose_name='techniques', blank=True),
        ),
    ]
