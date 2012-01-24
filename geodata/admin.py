from django.contrib.gis import admin
from models import  *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class InterestingLocationAdmin(admin.OSMGeoAdmin):
    list_display = ('name','interestingness')
    list_filter = ('name','interestingness',)
    fieldsets = (
        ('Location Attributes', {'fields': (('name','interestingness'))}),
        ('Editable Map View', {'fields': ('geometry',)}),
    )

    # Default GeoDjango OpenLayers map options
    scrollable = False
    map_width = 700
    map_height = 325
    if settings.OPENLAYERS:
      openlayers_url = settings.OPENLAYERS

admin.site.register(InterestingLocation, InterestingLocationAdmin)

class EarthGeoDataAdmin(admin.OSMGeoAdmin):
    list_display = ('name','pub_date','creator','interestingness')
    list_filter = ('name','pub_date','creator','interestingness')
    search_fields = ['creator__user__username','name']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name','pub_date','creator','description','image','url','contact','interestingness'))}),
        ('Editable Map View', {'fields': ('geometry',)}),
    )

    # Default GeoDjango OpenLayers map options
    scrollable = False
    map_width = 700
    map_height = 325
    if settings.OPENLAYERS:
      openlayers_url = settings.OPENLAYERS

admin.site.register(EarthGeoData, EarthGeoDataAdmin)
