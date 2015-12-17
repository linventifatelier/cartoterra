"""GeoData forms."""

from django import forms
from models import GeoDataAbstract, Building, Worksite, Event, Stakeholder, \
    Image, EarthTechnique
from django.forms import ModelForm
from django.forms.models import ModelMultipleChoiceField, ModelChoiceIterator
from PIL.ExifTags import TAGS, GPSTAGS
from geodata.widgets import GeoDataWidget, BootstrapDatePicker, \
    EarthTechniqueMultiple, IsceahCheckboxInput
from django.contrib.contenttypes.forms import generic_inlineformset_factory
import logging
from django.contrib.gis.forms.fields import PointField
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict


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
        # try:
        #     iptc = IptcImagePlugin.getiptcinfo(i)
        #     ret['caption'] = iptc[(2,120)]
        #     ret['copyright'] = iptc[(2,116)]
        #     ret['keywords'] = iptc[(2,25)]
        # except:
        #     ret['headline'] = None
        #     ret['caption'] = None
        #     ret['copyright'] = None
        #     ret['keywords'] = []

    ret['latitude'] = lat
    ret['longitude'] = lon
    ret['altitude'] = altitude
    ret[decoded] = gps_data

    return ret

##############################################


class EarthTechniqueChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (
            self.field.prepare_value(obj),
            self.field.label_from_instance(obj),
            obj
        )


class EarthTechniqueMultipleChoiceField(ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(EarthTechniqueMultipleChoiceField, self).__init__(
            *args, **kwargs
        )
        self.choices = EarthTechniqueChoiceIterator(self)


ImageFormSet = generic_inlineformset_factory(Image, extra=1, can_delete=True)


class GeoDataAbstractForm(ModelForm):
    geometry = PointField(widget=GeoDataWidget())
    # geometry = forms.CharField(widget=GeodataWidget())
    # def clean(self):
    #     super(MapModelForm, self).clean()
    #
    #     if not self.cleaned_data['geometry']:
    #         if self.cleaned_data['image']:
    #             im = Image.open(self.cleaned_data['image'])
    #             gps_data = _get_exifgps(im)
    #             longitude = gps_data['longitude']
    #             latitude = gps_data['latitude']
    #             if longitude and latitude:
    #                 try:
    #                     self.cleaned_data['geometry'] =
    #                         Point(longitude, latitude)
    #                 except (ValueError, TypeError):
    #                     msg = _("You have to provide a geometry or a \
    #                              geolocated image (the geolocation data of \
    #                              your image do not seem clean).")
    #                     self._errors['geometry'] = self.error_class([msg])
    #             else:
    #                 msg = _("You have to provide a geometry \
    #                          or a geolocated image (the image you have \
    #                          provided does not seems to be geolocated).")
    #                 self._errors['geometry'] = self.error_class([msg])
    #         else:
    #             msg = _("You have to provide a geometry or a geolocated \
    #                      image.")
    #             self._errors['geometry'] = self.error_class([msg])
    #     return self.cleaned_data

    class Meta:
        model = GeoDataAbstract
        exclude = ('creator', 'pub_date', )

    class Media:
        js = ('js/formset.js', )


# https://stackoverflow.com/questions/913589/django-forms-inheritance-and-order-of-form-fields/27493844#27493844
def reorder_fields(fields, order):
    """Reorder form fields by order, removing items not in order.

    >>> reorder_fields(
    ...     OrderedDict([('a', 1), ('b', 2), ('c', 3)]),
    ...     ['b', 'c', 'a'])
    OrderedDict([('b', 2), ('c', 3), ('a', 1)])
    """
    for key, v in fields.items():
        if key not in order:
            del fields[key]

    return OrderedDict(sorted(fields.items(), key=lambda k: order.index(k[0])))


class BuildingForm(GeoDataAbstractForm):
    detailed_description = forms.CharField(
        required=False, widget=forms.Textarea,
        help_text=_("Detailled description (major elements, present and past \
use, cultural affiliation, historical/cultural/architectural \
importance, period of construction, geographical scole, associated \
events, hybrid construction techniques if any)")
    )
    inauguration_date = forms.DateField(
        required=False, widget=BootstrapDatePicker,
        help_text=_("Put here the inauguration date for a contemporary \
building if known, ignore otherwise.")
    )
    construction_date = forms.CharField(
        required=False, help_text=_("If heritage site")
    )
    isceah = forms.BooleanField(
        required=False, widget=IsceahCheckboxInput,
        help_text=_("Tick here if you are member of ICOMOS-ISCEAH and want \
this entry to be referenced as ICOMOS-ISCEAH.")
    )
    techniques = EarthTechniqueMultipleChoiceField(
        required=False, queryset=EarthTechnique.objects.all(),
        widget=EarthTechniqueMultiple
    )
    stakeholder = forms.ModelMultipleChoiceField(
        required=False, queryset=Stakeholder.objects.all(),
        help_text=_("Select cartoterra.net stakeholders you want to link to \
this entry.")
    )

    def __init__(self, user=None, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        if not user.has_perm('profile.world_heritage'):
            self.fields['unesco'].widget.attrs['disabled'] = 'disabled'
        self._user = user
        # https://stackoverflow.com/questions/913589/django-forms-inheritance-and-order-of-form-fields/27493844#27493844
        key_order = [
            'name', 'geometry', 'heritage_status', 'isceah',
            'classification', 'use', 'cultural_landscape', 'unesco',
            'protection_status', 'property_status', 'techniques',
            'earth_quantity', 'description', 'detailed_description',
            'inauguration_date', 'construction_date', 'condition',
            'references', 'url', 'architects', 'stakeholder', 'contact',
            'credit_creator', 'image'
        ]
        self.fields = reorder_fields(self.fields, key_order)

        for f in [
            'detailed_description',
            'classification', 'use', 'cultural_landscape',
            'protection_status', 'property_status', 'construction_date',
            'condition', 'references'
        ]:
            self.fields[f].widget.attrs['class'] = 'geodata-isceah'
        self.fields['isceah'].widget.attrs['class'] = 'geodata-toggle-isceah'

    def clean_unesco(self):
        if self._user.has_perm('profile.world_heritage'):
            return self.cleaned_data.get('unesco')
        else:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                return instance.unesco
            else:
                return self.fields['unesco'].initial

    class Meta:
        model = Building
        exclude = ('creator', 'pub_date', )


class WorksiteForm(GeoDataAbstractForm):
    inauguration_date = forms.DateField(
        widget=BootstrapDatePicker, required=False
    )
    techniques = EarthTechniqueMultipleChoiceField(
        required=False, queryset=EarthTechnique.objects.all(),
        widget=EarthTechniqueMultiple,
    )

    def __init__(self, user=None, *args, **kwargs):
        super(WorksiteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Worksite
        exclude = ('creator', 'pub_date', )


class EventForm(GeoDataAbstractForm):
    beginning_date = forms.DateField(widget=BootstrapDatePicker)
    end_date = forms.DateField(widget=BootstrapDatePicker)

    def __init__(self, user=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if not user.has_perm('profile.unesco_chair'):
            self.fields['unesco_chair'].widget.attrs['disabled'] = 'disabled'
        self._user = user

    def clean_unesco_chair(self):
        if self._user.has_perm('profile.unesco_chair'):
            return self.cleaned_data.get('unesco_chair')
        else:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                return instance.unesco_chair
            else:
                return self.fields['unesco_chair'].initial

    class Meta:
        model = Event
        exclude = ('creator', 'pub_date', )


class StakeholderForm(GeoDataAbstractForm):
    isceah = forms.BooleanField(
        help_text=_("Tick here if you are member of ICOMOS-ISCEAH and want \
this entry to be referenced as ICOMOS-ISCEAH.")
    )

    def __init__(self, user=None, *args, **kwargs):
        super(StakeholderForm, self).__init__(*args, **kwargs)
        if not user.has_perm('profile.unesco_chair'):
            self.fields['unesco_chair'].widget.attrs['disabled'] = 'disabled'
        self._user = user

    def clean_unesco_chair(self):
        if self._user.has_perm('profile.unesco_chair'):
            return self.cleaned_data.get('unesco_chair')
        else:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                return instance.unesco_chair
            else:
                return self.fields['unesco_chair'].initial

    class Meta:
        model = Stakeholder
        exclude = ('creator', 'pub_date', )
