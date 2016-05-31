from models import Question
from django.contrib import admin
from hvad import admin as hvadadmin


class QuestionAdmin(hvadadmin.TranslatableAdmin):
    """Question administration interface."""

admin.site.register(Question, QuestionAdmin)
