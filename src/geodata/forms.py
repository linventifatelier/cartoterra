"""GeoData forms."""

from django import forms
from olwidget.forms import MapModelForm
from models import EarthGeoDataMeeting, EarthGeoDataPatrimony, \
     EarthGeoDataConstruction


class EarthGeoDataPatrimonyForm(MapModelForm):
    class Meta:
        model = EarthGeoDataPatrimony
