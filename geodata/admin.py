"""Geodata administration interface."""
from django.contrib.gis import admin
from models import Building, Worksite, Event, Stakeholder, Image, \
    EventType, EarthTechnique, EarthRole
#from django.conf import settings
#from stdimage import StdImageField
from imagewidget import AdminImageWidget
#from forms import EarthGeoDataAbstractForm
#from sorl.thumbnail.admin import AdminImageMixin
#from sorl.thumbnail import get_thumbnail
#from widget import AdminImageFieldWithThumbWidget

#ADMIN_THUMBS_SIZE = '60x60'
#from nani import admin
from hvad import admin as hvadadmin
from django.contrib.contenttypes.generic import GenericTabularInline
from imagekit.admin import AdminThumbnail


# class MyModelAdmin(admin.ModelAdmin):
# #    model = models.MyModel
#     list_display = ['image', ]

#     def my_image_thumb(self, obj):
#         if obj.image:
#             thumb = get_thumbnail(obj.image.file, ADMIN_THUMBS_SIZE)
#             return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
#         else:
#             return "No Image"
#     my_image_thumb.short_description = 'My Thumbnail'
#     my_image_thumb.allow_tags = True


#class MyModelAdmin(AdminImageMixin, admin.ModelAdmin):
#    pass


class EarthAdmin(admin.ModelAdmin):
    """Modified admin.ModelAdmin (include special AdminImageWidget for the
    image field)."""
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            #request = kwargs.pop("request", None)
            #_request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(EarthAdmin, self).formfield_for_dbfield(db_field,
                                                             **kwargs)


class EarthOSMAdmin(admin.OSMGeoAdmin):
    """Modified admin.OSMGeoAdmin (include special AdminImageWidget for the
    image field). TODO: does not work."""
    #def formfield_for_dbfield(self, db_field, **kwargs):
    #    if db_field.name == 'image':
    #        #request = kwargs.pop("request", None)
    #        _request = kwargs.pop("request", None)
    #        kwargs['widget'] = AdminImageWidget
    #        return db_field.formfield(**kwargs)
    #    return super(EarthOSMAdmin, self).formfield_for_dbfield(db_field,
    #                                                         **kwargs)
    openlayers_url = 'openlayers/OpenLayers.js'


class EarthRoleAdmin(hvadadmin.TranslatableAdmin):
#class EarthTechniqueAdmin(MyAdmin):
    """EarthRole administration interface."""
    #list_display = ['name']
    #list_filter = ['name']
    #search_fields = ['name']

    fieldsets = (
        #('Roles', {'fields': (('name', ))}),
        #('Techniques', {'fields': (('name', 'description', 'image', 'url'))}),
    )

admin.site.register(EarthRole, EarthRoleAdmin)


class EarthTechniqueAdmin(admin.ModelAdmin):
#class EarthTechniqueAdmin(MyAdmin):
#class EarthTechniqueAdmin(MyModelAdmin):
#class EarthTechniqueAdmin(MyAdmin):
    """EarthTechnique administration interface."""
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

    fieldsets = (
        ('Techniques', {'fields': (('name', 'description', 'url'))}),
        #('Techniques', {'fields': (('name', 'description', 'image', 'url'))}),
    )

admin.site.register(EarthTechnique, EarthTechniqueAdmin)


class EventTypeAdmin(hvadadmin.TranslatableAdmin):
    """EarthMeetingType administration interface."""
    #list_display = ['ident_name']
    #list_filter = ['ident_name']
    #search_fields = ['name']

    fieldsets = (
        #('Identification Name', {'fields': (('ident_name', ))}),
        #('Techniques', {'fields': (('name', 'description', 'image', 'url'))}),
    )

admin.site.register(EventType, EventTypeAdmin)


class ImageInline(GenericTabularInline):
    model = Image
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    readonly_fields = ('admin_thumbnail', )


#class EarthGeoDataAbstractAdmin(MyOSMAdmin):
#class EarthGeoDataAbstractAdmin(admin.OSMGeoAdmin):
class GeoDataAbstractAdmin(EarthOSMAdmin):
    """EarthGeoData abstract administration interface."""
    list_display = ('name', 'pub_date', 'creator')
    list_filter = ('name', 'pub_date', 'creator')
    search_fields = ['creator__username', 'name']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'creator',
                                             'description',
                                             'url', 'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )
    inlines = [ImageInline]

    # Default GeoDjango OpenLayers map options
    #scrollable = False
    #map_width = 700
    #map_height = 325
    #if settings.OPENLAYERS:
    #    openlayers_url = settings.OPENLAYERS

    class Meta:
        """Abstract class."""
        abstract = True


class StakeholderAdmin(GeoDataAbstractAdmin):
    """EarthGeoDataActor administration interface."""
    list_display = ('name', 'pub_date', 'creator')
    list_filter = ('name', 'pub_date', 'creator', 'role')
    search_fields = ['creator__username', 'name', 'role']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'creator', 'role',
                                             'description', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(Stakeholder, StakeholderAdmin)


class BuildingAdmin(GeoDataAbstractAdmin):
    """EarthGeoDataPatrimony administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator', 'unesco')
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator',
                   'inauguration_date', 'architects', 'techniques', 'unesco',
                   'stakeholder')
    search_fields = ['creator__username', 'name', 'techniques', 'architects',
                     'stakeholder']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'inauguration_date', 'creator',
                                             'credit_creator', 'architects',
                                             'techniques', 'stakeholder',
                                             'unesco', 'description', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(Building, BuildingAdmin)


class EventAdmin(GeoDataAbstractAdmin):
    """EarthGeoDataMeeting administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator',
                    'event_type', 'beginning_date', 'end_date', )
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator',
                   'event_type', 'beginning_date', 'end_date',
                   'stakeholder')
    search_fields = ['creator__username', 'name', 'event_type',
                     'stakeholder']
    date_hierarchy = 'beginning_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'event_type',
                                             'pub_date', 'beginning_date',
                                             'end_date', 'creator',
                                             'credit_creator', 'stakeholder',
                                             'description', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(Event, EventAdmin)


class WorksiteAdmin(GeoDataAbstractAdmin):
    """EarthGeoDataConstruction administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator',
                    'participative', )
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator',
                   'participative', 'inauguration_date', 'techniques',
                   'stakeholder')
    search_fields = ['creator__username', 'name', 'techniques', 'stakeholder']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date', 'creator',
                                             'credit_creator', 'stakeholder',
                                             'participative', 'techniques',
                                             'description', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(Worksite, WorksiteAdmin)
