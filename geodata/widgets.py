from geodata.models import GeoDataAbstract
from django.contrib.gis import admin


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
