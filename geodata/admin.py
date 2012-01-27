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


class EarthTechniqueAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fieldsets = (
        ('Techniques', {'fields': (('name','description','image','url'))}),
    )

admin.site.register(EarthTechnique, EarthTechniqueAdmin)


class EarthArchitectAdmin(admin.ModelAdmin):
    list_display = ['name','user']
    list_filter = ['name','user']
    search_fields = ['name']
    fieldsets = (
        ('Architect', {'fields': (('name','user'))}),
    )

admin.site.register(EarthArchitect, EarthArchitectAdmin)

class EarthMeetingAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fieldsets = (
        ('Type of meeting', {'fields': (('name',))}),
    )

admin.site.register(EarthMeeting, EarthMeetingAdmin)

class EarthGeoDataAbstractAdmin(admin.OSMGeoAdmin):
    list_display = ('name','pub_date','creator')
    list_filter = ('name','pub_date','creator')
    search_fields = ['creator__username','name']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name','pub_date','creator','description','image','url','contact'))}),
        ('Editable Map View', {'fields': ('geometry',)}),
    )

    # Default GeoDjango OpenLayers map options
    scrollable = False
    map_width = 700
    map_height = 325
    if settings.OPENLAYERS:
        openlayers_url = settings.OPENLAYERS

    class Meta:
        abstract = True


class EarthGeoDataPatrimonyAdmin(EarthGeoDataAbstractAdmin):
    list_display = ('name','pub_date','creator','unesco')
    list_filter = ('name','pub_date','inauguration_date','creator','architects','techniques','unesco')
    search_fields = ['creator__username','name','techniques','architects']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name','pub_date','inauguration_date','creator','architects','techniques','unesco','description','image','url','contact'))}),
        ('Editable Map View', {'fields': ('geometry',)}),
    )

admin.site.register(EarthGeoDataPatrimony, EarthGeoDataPatrimonyAdmin)


class EarthGeoDataMeetingAdmin(EarthGeoDataAbstractAdmin):
    list_display = ('name','meeting','beginning_date','end_date','creator')
    list_filter = ('name','meeting','pub_date','beginning_date','end_date','creator')
    search_fields = ['creator__username','name','meeting']
    date_hierarchy = 'beginning_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name','meeting','pub_date','beginning_date','end_date','creator','description','image','url','contact'))}),
        ('Editable Map View', {'fields': ('geometry',)}),
    )

admin.site.register(EarthGeoDataMeeting, EarthGeoDataMeetingAdmin)


class EarthGeoDataConstructionAdmin(EarthGeoDataAbstractAdmin):
    list_display = ('name','participative','creator')
    list_filter = ('name','participative','pub_date','techniques','creator')
    search_fields = ['creator__username','name','techniques']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name','pub_date','creator','participative','techniques','description','image','url','contact'))}),
        ('Editable Map View', {'fields': ('geometry',)}),
    )

admin.site.register(EarthGeoDataConstruction, EarthGeoDataConstructionAdmin)
