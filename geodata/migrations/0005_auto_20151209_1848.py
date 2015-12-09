# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0004_delete_buildingculturallandscape'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buildingpropertystatus',
            options={'verbose_name': 'building property status', 'verbose_name_plural': 'building property statuses'},
        ),
        migrations.AlterModelOptions(
            name='buildingprotectionstatus',
            options={'verbose_name': 'building protection status', 'verbose_name_plural': 'building protection statuses'},
        ),
        migrations.AlterModelOptions(
            name='earthquantity',
            options={'verbose_name': 'earthen material quantity', 'verbose_name_plural': 'earthen material quantities'},
        ),
        migrations.AddField(
            model_name='building',
            name='classification',
            field=models.ForeignKey(verbose_name='classification', blank=True, to='geodata.BuildingClassification', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='condition',
            field=models.TextField(null=True, verbose_name='site condition and threats', blank=True),
        ),
        migrations.AddField(
            model_name='building',
            name='construction_date',
            field=models.CharField(max_length=50, null=True, verbose_name='Approximative construction date', blank=True),
        ),
        migrations.AddField(
            model_name='building',
            name='cultural_landscape',
            field=models.NullBooleanField(default=None, verbose_name='cultural landscape', choices=[(None, b''), (True, 'Yes'), (False, 'No')]),
        ),
        migrations.AddField(
            model_name='building',
            name='earth_quantity',
            field=models.ForeignKey(verbose_name='quantity of earthen material in the structure', blank=True, to='geodata.EarthQuantity', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='property_status',
            field=models.ForeignKey(verbose_name='property status', blank=True, to='geodata.BuildingPropertyStatus', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='protection_status',
            field=models.ForeignKey(verbose_name='protection status', blank=True, to='geodata.BuildingProtectionStatus', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='references',
            field=models.TextField(null=True, verbose_name='principal references', blank=True),
        ),
        migrations.AddField(
            model_name='building',
            name='use',
            field=models.ForeignKey(verbose_name='use', blank=True, to='geodata.BuildingUse', null=True),
        ),
    ]
