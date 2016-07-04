# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0017_auto_20160626_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='simple',
            field=models.BooleanField(default=False, verbose_name='simple building'),
        ),
    ]
