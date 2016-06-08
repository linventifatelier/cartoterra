from django.db import models
from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields
import markdown


class Question(TranslatableModel):
    """FAQ Question"""
    translations = TranslatedFields(
        question_markdown=models.TextField(help_text=_('Use Markdown syntax.')),
        question=models.TextField(blank=True, null=True, editable=False),
        answer_markdown=models.TextField(help_text=_('Use Markdown syntax.')),
        answer=models.TextField(blank=True, null=True, editable=False),
    )

    def __unicode__(self):
        return self.safe_translation_getter('question_markdown', str(self.pk))

    def save(self):
        self.question = markdown.markdown(self.question_markdown)
        self.answer = markdown.markdown(self.answer_markdown)
        super(Question, self).save()
