from django.contrib.gis.admin.widgets import OpenLayersWidget
from geodata.models import EarthGeoDataAbstract
from django.contrib.gis import admin

class PointAdmin(admin.OSMGeoAdmin):
    list_filter = ('content_type','geometry' )
    list_display = ('object', 'geometry', 'content_type', 'object_id')
    map_template = 'geodata/geodata_form_geometry_widget.html'

# Getting an instance so we can generate the map widget; also
# getting the geometry field for the model.
admin_instance = PointAdmin(EarthGeoDataAbstract, admin.site)
point_field = EarthGeoDataAbstract._meta.get_field('geometry')

# Generating the widget.
GeoDataWidget = admin_instance.get_map_widget(point_field)
