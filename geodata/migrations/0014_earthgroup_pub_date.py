# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0013_auto_20160614_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='earthgroup',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date'),
        ),
    ]
