# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0006_auto_20151209_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='detailed_description',
            field=models.TextField(null=True, verbose_name='detailed description', blank=True),
        ),
    ]
