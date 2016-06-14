from models import Question
from django.contrib import admin
from hvad.forms import TranslatableModelForm
from hvad.admin import TranslatableAdmin
from pagedown.widgets import AdminPagedownWidget


class QuestionAdminForm(TranslatableModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionAdminForm, self).__init__(*args, **kwargs)
        self.fields['question_markdown'].widget = AdminPagedownWidget()
        self.fields['answer_markdown'].widget = AdminPagedownWidget()


class QuestionAdmin(TranslatableAdmin):
    """Question administration interface."""
    form = QuestionAdminForm

admin.site.register(Question, QuestionAdmin)
