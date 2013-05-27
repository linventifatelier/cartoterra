from haystack import indexes
from geodata.models import Building, Worksite, Event, Stakeholder
from django.utils.timezone import now


class BuildingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='creator')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Building

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return Building.objects.filter(pub_date__lte=now())


class WorksiteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='creator')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Worksite

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return Worksite.objects.filter(pub_date__lte=now())


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='creator')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return Event.objects.filter(pub_date__lte=now())


class StakeholderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='creator')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Stakeholder

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return Stakeholder.objects.filter(pub_date__lte=now())
