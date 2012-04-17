"""GeoData forms."""

#from django import forms
import floppyforms as forms
from olwidget.forms import MapModelForm
from models import EarthGeoDataMeeting, EarthGeoDataPatrimony, \
     EarthGeoDataConstruction
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class DatePicker(forms.DateInput):
    template_name = 'datepicker.html'

    class Media:
        js = (
            'jquery-ui/js/jquery-ui-1.8.18.custom.min.js',
        )
        css = {
            'all': (
                'jquery-ui/css/ui-lightness/jquery-ui-1.8.18.custom.css',
            )
        }


class EarthGeoDataPatrimonyForm(MapModelForm):
    inauguration_date = forms.DateField(widget=DatePicker, required=False)
    class Meta:
        model = EarthGeoDataPatrimony
        exclude = ('creator', 'pub_date', )


class EarthGeoDataConstructionForm(MapModelForm):
    inauguration_date = forms.DateField(widget=DatePicker, required=False)
    class Meta:
        model = EarthGeoDataConstruction
        exclude = ('creator', 'pub_date', )

class EarthGeoDataMeetingForm(MapModelForm):
    beginning_date = forms.DateField(widget=DatePicker)
    end_date = forms.DateField(widget=DatePicker)
    class Meta:
        model = EarthGeoDataMeeting
        exclude = ('creator', 'pub_date', )

