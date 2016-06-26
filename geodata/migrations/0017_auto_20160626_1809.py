# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0016_profile_r_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.RemoveField(
            model_name='building',
            name='unesco',
        ),
        migrations.RemoveField(
            model_name='event',
            name='unesco_chair',
        ),
        migrations.RemoveField(
            model_name='stakeholder',
            name='isceah',
        ),
        migrations.RemoveField(
            model_name='stakeholder',
            name='unesco_chair',
        ),
    ]
