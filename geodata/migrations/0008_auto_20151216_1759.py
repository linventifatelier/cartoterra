# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0007_building_detailed_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingConstructionStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='construction_status',
            field=models.ForeignKey(verbose_name='construction status', blank=True, to='geodata.BuildingConstructionStatus', null=True),
        ),
    ]
