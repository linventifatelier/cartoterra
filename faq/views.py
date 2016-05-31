from models import Question
from django.views.generic.list import ListView


class QuestionListView(ListView):
    model = Question
