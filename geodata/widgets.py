from geodata.models import GeoDataAbstract
from django.contrib.gis import admin
from django.forms.widgets import DateInput


class PointAdmin(admin.OSMGeoAdmin):
    list_filter = ('content_type', 'geometry')
    list_display = ('object', 'geometry', 'content_type', 'object_id')
    map_template = 'geodata/geodata_form_geometry_widget.html'

# Getting an instance so we can generate the map widget; also
# getting the geometry field for the model.
admin_instance = PointAdmin(GeoDataAbstract, admin.site)
point_field = GeoDataAbstract._meta.get_field('geometry')

# Generating the widget.
GeoDataWidget = admin_instance.get_map_widget(point_field)


class BootstrapDatePicker(DateInput):
    def __init__(self, attrs=None):
        if attrs is not None:
            if 'class' in attrs:
                attrs['class'] = 'form-datepicker ' + attrs['class']
            else:
                attrs['class'] = 'form-datepicker'
        else:
            attrs = {'class': 'form-datepicker', }
        super(BootstrapDatePicker, self).__init__(attrs)

    class Media:
        js = (
            'js/bootstrap-datepicker.js',
            'js/form-datepicker.js',
        )
        css = {
            'all': (
                'css/datepicker3.css',
            )
        }
