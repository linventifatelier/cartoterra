from django.db import models
from hvad.models import TranslatableModel, TranslatedFields


class Question(TranslatableModel):
    """FAQ Question"""
    translations = TranslatedFields(
        question=models.TextField(),
        answer=models.TextField()
    )

    def __unicode__(self):
        return self.safe_translation_getter('question', str(self.pk))
