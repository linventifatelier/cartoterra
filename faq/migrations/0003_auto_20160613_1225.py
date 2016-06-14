# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20160608_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questiontranslation',
            name='answer',
            field=models.TextField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='questiontranslation',
            name='question',
            field=models.TextField(null=True, editable=False, blank=True),
        ),
    ]
