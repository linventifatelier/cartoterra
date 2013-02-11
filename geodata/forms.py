"""GeoData forms."""

#from django import forms
import floppyforms as forms
from models import EarthGeoDataAbstract, EarthGeoDataMeeting, \
    EarthGeoDataPatrimony, EarthGeoDataConstruction, EarthGeoDataActor
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import ModelForm
from sorl.thumbnail import ImageField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from PIL.ExifTags import TAGS, GPSTAGS
from sorl.thumbnail import ImageField
import PIL.Image
from django.utils.translation import ugettext_lazy as _
from geodata.widgets import GeoDataWidget




##############################################
# Credits:
# https://bitbucket.org/weholt/django-photofile/
# http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/
# http://eran.sandler.co.il/2011/05/20/extract-gps-latitude-and-longitude-data-from-exif-using-python-imaging-library-pil/
def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _fractToSimple(frac):
    if not frac:
        return None
    try:
        f,n = frac
        return round(float(f) / float(n), 3)
    except Exception, e:
        return None


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
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


def _get_exifgps(i):
    ret = {}
    #i = Image.open(fn)

    lat = None
    lon = None
    altitude = None

    info = i._getexif()

    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            #print "TAG", decoded, value
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                ret[decoded] = gps_data

                gps_latitude = _get_if_exist(gps_data, "GPSLatitude")
                gps_latitude_ref = _get_if_exist(gps_data, 'GPSLatitudeRef')
                gps_longitude = _get_if_exist(gps_data, 'GPSLongitude')
                gps_longitude_ref = _get_if_exist(gps_data, 'GPSLongitudeRef')

                if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                    lat = _convert_to_degress(gps_latitude)
                    if gps_latitude_ref != "N":
                        lat = 0 - lat

                    lon = _convert_to_degress(gps_longitude)
                    if gps_longitude_ref != "E":
                        lon = 0 - lon

                altitude = _get_if_exist(gps_data, 'GPSAltitude')
                if altitude:
                    altitude = _fractToSimple(altitude)
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

    return ret

##############################################


class DatePicker(forms.DateInput):
    template_name = 'datepicker.html'

    class Media:
        js = (
            'jquery-ui/js/jquery-ui-1.9.1.custom.min.js',
        )
        css = {
            'all': (
                'jquery-ui/css/ui-lightness/jquery-ui-1.9.1.custom.min.css',
            )
        }


#class ImageWidget(forms.FileInput):
#    """
#    A ImageField Widget that shows a thumbnail.
#    """
#
#    def __init__(self, attrs={}):
#        super(ImageWidget, self).__init__(attrs)
#
#    def render(self, name, value, attrs=None):
#        output = []
#        if value and hasattr(value, "url"):
#            output.append(('<a rel="facebox" target="_blank" href="%s">'
#                           '<img class="photo" src="%s" style="height: 100px;" /></a> <br/>'
#                           % (value.url, value.url)))
#        output.append(super(ImageWidget, self).render(name, value, attrs))
#        return mark_safe(u''.join(output))


class EarthGeoDataAbstractForm(ModelForm):
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
    #                    self.cleaned_data['geometry'] = Point(longitude, latitude)
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
        model = EarthGeoDataAbstract
        exclude = ('creator', 'pub_date', )
    
    class Media:
        css = {
            'all': ('css/geodata.css', )
        }
        js = ('openlayers/OpenLayers.js', )



class EarthGeoDataPatrimonyForm(EarthGeoDataAbstractForm):
    inauguration_date = forms.DateField(widget=DatePicker, required=False)

    class Meta:
        model = EarthGeoDataPatrimony
        exclude = ('creator', 'pub_date', )


class EarthGeoDataConstructionForm(EarthGeoDataAbstractForm):
    inauguration_date = forms.DateField(widget=DatePicker, required=False)

    class Meta:
        model = EarthGeoDataConstruction
        exclude = ('creator', 'pub_date', )


class EarthGeoDataMeetingForm(EarthGeoDataAbstractForm):
    beginning_date = forms.DateField(widget=DatePicker)
    end_date = forms.DateField(widget=DatePicker)
    class Meta:
        model = EarthGeoDataMeeting
        exclude = ('creator', 'pub_date', )


class EarthGeoDataActorForm(EarthGeoDataAbstractForm):
    class Meta:
        model = EarthGeoDataActor
        exclude = ('creator', 'pub_date', )

