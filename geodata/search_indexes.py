from haystack import indexes
from haystack import site
from geodata.models import EarthGeoDataPatrimony
from geodata.models import EarthGeoDataConstruction
from geodata.models import EarthGeoDataMeeting
from django.utils.timezone import now


class EarthGeoDataPatrimonyIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='creator')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return EarthGeoDataPatrimony

    def index_queryset(self):
        "Used when the entire index for model is updated."
        return EarthGeoDataPatrimony.objects.filter(pub_date__lte=now())


site.register(EarthGeoDataPatrimony, EarthGeoDataPatrimonyIndex)


class EarthGeoDataConstructionIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='creator')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return EarthGeoDataConstruction

    def index_queryset(self):
        "Used when the entire index for model is updated."
        return EarthGeoDataConstruction.objects.filter(pub_date__lte=now())


site.register(EarthGeoDataConstruction, EarthGeoDataConstructionIndex)


class EarthGeoDataMeetingIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='creator')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return EarthGeoDataMeeting

    def index_queryset(self):
        "Used when the entire index for model is updated."
        return EarthGeoDataMeeting.objects.filter(pub_date__lte=now())


site.register(EarthGeoDataMeeting, EarthGeoDataMeetingIndex)
