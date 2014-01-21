from django.contrib.gis.forms.widgets import OSMWidget
from django.forms.widgets import DateInput


class GeoDataWidget(OSMWidget):
    template_name = 'geodata/geodata_form_geometry_widget.html'

    class Media:
        js = (
            'js/spin.min.js',
            'js/form-geometry.js',
        )


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
