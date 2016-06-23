# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiontranslation',
            name='answer_markdown',
            field=models.TextField(default='', help_text='Use Markdown syntax.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questiontranslation',
            name='question_markdown',
            field=models.TextField(default='', help_text='Use Markdown syntax.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='questiontranslation',
            name='answer',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questiontranslation',
            name='question',
            field=models.TextField(null=True, blank=True),
        ),
    ]
