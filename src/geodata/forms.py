"""GeoData forms."""

from django import forms
from olwidget.forms import MapModelForm
from models import EarthGeoDataMeeting, EarthGeoDataPatrimony, \
     EarthGeoDataConstruction
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class EarthGeoDataPatrimonyForm(MapModelForm):
    class Meta:
        model = EarthGeoDataPatrimony
        exclude = ('creator', 'pub_date', )


class EarthGeoDataConstructionForm(MapModelForm):
    class Meta:
        model = EarthGeoDataConstruction
        exclude = ('creator', 'pub_date', )

class EarthGeoDataMeetingForm(MapModelForm):
    class Meta:
        model = EarthGeoDataMeeting
        exclude = ('creator', 'pub_date', )

