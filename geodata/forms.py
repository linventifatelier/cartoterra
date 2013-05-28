"""GeoData forms."""

#from django import forms
import floppyforms as forms
from models import GeoDataAbstract, Building, Worksite, Event, Stakeholder, \
    Image
from django.forms import ModelForm
from PIL.ExifTags import TAGS, GPSTAGS
from geodata.widgets import GeoDataWidget
from django.contrib.contenttypes.generic import generic_inlineformset_factory
import logging

logger = logging.getLogger(__name__)


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _frac_to_float(frac):
    try:
        f, n = frac
        return round(float(f) / float(n), 3)
    except:
        logger.warning("_get_exifgps: Conversion of altitude from frac to \
            float failed. Exif altitude: %s" % frac)
        return None


def _convert_to_degress(value):
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def _extract_gpsinfo(values):
    lat = None
    lon = None
    altitude = None
    gps_data = {}
    for t in values:
        sub_decoded = GPSTAGS.get(t, t)
        gps_data[sub_decoded] = values[t]

    gps_lat = _get_if_exist(gps_data, "GPSLatitude")
    gps_lat_ref = _get_if_exist(gps_data, 'GPSLatitudeRef')
    gps_lon = _get_if_exist(gps_data, 'GPSLongitude')
    gps_lon_ref = _get_if_exist(gps_data, 'GPSLongitudeRef')

    if gps_lat and gps_lat_ref and gps_lon and gps_lon_ref:
        lat = _convert_to_degress(gps_lat)
        if gps_lat_ref != "N":
            lat = 0 - lat

        lon = _convert_to_degress(gps_lon)
        if gps_lon_ref != "E":
            lon = 0 - lon

    altitude = _get_if_exist(gps_data, 'GPSAltitude')
    if altitude:
        altitude = _frac_to_float(altitude)
    return (lat, lon, altitude, gps_data)


def _get_exifgps(i):
    ret = {}

    info = i._getexif()

    if info:
        for tag, values in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                lat, lon, altitude, gps_data = _extract_gpsinfo(values)
        #try:
        #    iptc = IptcImagePlugin.getiptcinfo(i)
        #    ret['caption'] = iptc[(2,120)]
        #    ret['copyright'] = iptc[(2,116)]
        #    ret['keywords'] = iptc[(2,25)]
        #except:
        #    ret['headline'] = None
        #    ret['caption'] = None
        #    ret['copyright'] = None
        #    ret['keywords'] = []

    ret['latitude'] = lat
    ret['longitude'] = lon
    ret['altitude'] = altitude
    ret[decoded] = gps_data

    return ret

##############################################


class DatePicker(forms.DateInput):
    template_name = 'datepicker.html'

    class Media:
        js = (
            'js/jquery-ui-1.10.3.custom.min.js',
            'js/modernizr.custom.min.js',
        )
        css = {
            'all': (
                'css/ui-lightness/jquery-ui-1.10.3.custom.min.css',
            )
        }


ImageFormSet = generic_inlineformset_factory(Image, extra=1, can_delete=True)


class GeoDataAbstractForm(ModelForm):
    geometry = forms.CharField(widget=GeoDataWidget())
    #geometry = forms.CharField(widget=GeodataWidget())
    #def clean(self):
    #    super(MapModelForm, self).clean()

    #    if not self.cleaned_data['geometry']:
    #        if self.cleaned_data['image']:
    #            im = Image.open(self.cleaned_data['image'])
    #            gps_data = _get_exifgps(im)
    #            longitude = gps_data['longitude']
    #            latitude = gps_data['latitude']
    #            if longitude and latitude:
    #                try:
    #                    self.cleaned_data['geometry'] =
    #                        Point(longitude, latitude)
    #                except (ValueError, TypeError):
    #                    msg = _("You have to provide a geometry or a \
    #                             geolocated image (the geolocation data of \
    #                             your image do not seem clean).")
    #                    self._errors['geometry'] = self.error_class([msg])
    #            else:
    #                msg = _("You have to provide a geometry \
    #                         or a geolocated image (the image you have \
    #                         provided does not seems to be geolocated).")
    #                self._errors['geometry'] = self.error_class([msg])
    #        else:
    #            msg = _("You have to provide a geometry or a geolocated \
    #                     image.")
    #            self._errors['geometry'] = self.error_class([msg])
    #    return self.cleaned_data

    class Meta:
        model = GeoDataAbstract
        exclude = ('creator', 'pub_date', )

    class Media:
        js = ('openlayers/OpenLayers.js', 'js/formset.js', 'js/spin.min.js', )


class BuildingForm(GeoDataAbstractForm):
    inauguration_date = forms.DateField(widget=DatePicker, required=False)

    class Meta:
        model = Building
        exclude = ('creator', 'pub_date', )


class WorksiteForm(GeoDataAbstractForm):
    inauguration_date = forms.DateField(widget=DatePicker, required=False)

    class Meta:
        model = Worksite
        exclude = ('creator', 'pub_date', )


class EventForm(GeoDataAbstractForm):
    beginning_date = forms.DateField(widget=DatePicker)
    end_date = forms.DateField(widget=DatePicker)

    class Meta:
        model = Event
        exclude = ('creator', 'pub_date', )


class StakeholderForm(GeoDataAbstractForm):

    class Meta:
        model = Stakeholder
        exclude = ('creator', 'pub_date', )
