# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0008_auto_20151216_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buildingconstructionstatus',
            options={'verbose_name': 'building construction status', 'verbose_name_plural': 'building construction statuses'},
        ),
    ]
