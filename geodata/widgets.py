from django.forms.widgets import DateInput
from leaflet.forms.widgets import LeafletWidget


class GeoDataWidget(LeafletWidget):
    include_media = True
    template_name = 'geodata/geodata_form_geometry_widget.html'
    map_width = '500px'
    map_height = '250px'

    class Media:
        js = [
            'js/spin.min.js',
            'js/form-geometry.js',
        ]


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
            'js/bootstrap-datepicker.min.js',
            'js/form-datepicker.js',
        )
        css = {
            'all': (
                'css/bootstrap-datepicker3.min.css',
            )
        }
