# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0015_earthgroup_administrators'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='r_group',
            field=models.ManyToManyField(related_name='recommended_by', verbose_name='group recommendations', to='geodata.EarthGroup', blank=True),
        ),
    ]
