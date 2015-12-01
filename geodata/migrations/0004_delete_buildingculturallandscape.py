# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0003_buildingclassification_buildingculturallandscape_buildingpropertystatus_buildingprotectionstatus_bui'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BuildingCulturalLandscape',
        ),
    ]
