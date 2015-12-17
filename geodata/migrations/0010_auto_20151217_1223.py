# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0009_auto_20151216_1913'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BuildingConstructionStatus',
            new_name='BuildingHeritageStatus',
        ),
        migrations.AlterModelOptions(
            name='buildingheritagestatus',
            options={'verbose_name': 'building heritage status', 'verbose_name_plural': 'building heritage statuses'},
        ),
        migrations.RemoveField(
            model_name='building',
            name='construction_status',
        ),
        migrations.AddField(
            model_name='building',
            name='heritage_status',
            field=models.ForeignKey(verbose_name='heritage or contemporary', blank=True, to='geodata.BuildingHeritageStatus', null=True),
        ),
    ]
