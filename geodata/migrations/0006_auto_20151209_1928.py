# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0005_auto_20151209_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='cultural_landscape',
            field=models.NullBooleanField(default=None, verbose_name='cultural landscape', choices=[(None, b'---------'), (True, 'Yes'), (False, 'No')]),
        ),
    ]
