# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='earthroletranslation',
            options={'default_permissions': (), 'managed': True},
        ),
        migrations.AlterModelOptions(
            name='eventtypetranslation',
            options={'default_permissions': (), 'managed': True},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (('world_heritage', 'Can modify world heritage properties'), ('unesco_chair', 'Can modify UNESCO Chair Earthen Architecture'), ('isceah', 'Can modify ISCEAH properties'))},
        ),
        migrations.AddField(
            model_name='building',
            name='isceah',
            field=models.BooleanField(default=False, verbose_name='ISCEAH'),
        ),
        migrations.AddField(
            model_name='stakeholder',
            name='isceah',
            field=models.BooleanField(default=False, verbose_name='ISCEAH'),
        ),
    ]
