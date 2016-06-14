# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0012_earthgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='earthgroup',
            name='buildings',
            field=models.ManyToManyField(to='geodata.Building', blank=True),
        ),
        migrations.AddField(
            model_name='earthgroup',
            name='events',
            field=models.ManyToManyField(to='geodata.Event', blank=True),
        ),
        migrations.AddField(
            model_name='earthgroup',
            name='stakeholders',
            field=models.ManyToManyField(to='geodata.Stakeholder', blank=True),
        ),
        migrations.AddField(
            model_name='earthgroup',
            name='worksites',
            field=models.ManyToManyField(to='geodata.Worksite', blank=True),
        ),
    ]
