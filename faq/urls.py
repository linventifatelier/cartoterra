from django.conf.urls import url
from views import QuestionListView


urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name="faq")
]
