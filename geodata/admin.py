"""Geodata administration interface."""
from django.contrib.gis import admin
#from olwidget.admin import GeoModelAdmin
#from olwidget.admin import GeoModelAdmin
from models import *
from django.conf import settings
#from stdimage import StdImageField
from imagewidget import AdminImageWidget
from forms import EarthGeoDataAbstractForm
#from sorl.thumbnail.admin import AdminImageMixin
#from sorl.thumbnail import get_thumbnail
#from widget import AdminImageFieldWithThumbWidget

#ADMIN_THUMBS_SIZE = '60x60'
#from nani import admin
from hvad import admin as hvadadmin


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
            _request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(EarthAdmin, self).formfield_for_dbfield(db_field, **kwargs)


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
    openlayers_url='openlayers/OpenLayers.js'


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


class EarthMeetingTypeAdmin(hvadadmin.TranslatableAdmin):
    """EarthMeetingType administration interface."""
    #list_display = ['name']
    #list_filter = ['name']
    #search_fields = ['name']

    fieldsets = (
        #('Roles', {'fields': (('name', ))}),
        #('Techniques', {'fields': (('name', 'description', 'image', 'url'))}),
    )

admin.site.register(EarthMeetingType, EarthMeetingTypeAdmin)


#class EarthGeoDataAbstractAdmin(MyOSMAdmin):
#class EarthGeoDataAbstractAdmin(admin.OSMGeoAdmin):
#class EarthGeoDataAbstractAdmin(GeoModelAdmin):
class EarthGeoDataAbstractAdmin(EarthOSMAdmin):
    """EarthGeoData abstract administration interface."""
    list_display = ('name', 'pub_date', 'creator')
    list_filter = ('name', 'pub_date', 'creator')
    search_fields = ['creator__username', 'name']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'creator',
                                             'description', 'image',
                                             'url', 'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

    # Default GeoDjango OpenLayers map options
    #scrollable = False
    #map_width = 700
    #map_height = 325
    #if settings.OPENLAYERS:
    #    openlayers_url = settings.OPENLAYERS

    class Meta:
        """Abstract class."""
        abstract = True


class EarthGeoDataActorAdmin(EarthGeoDataAbstractAdmin):
    """EarthGeoDataActor administration interface."""
    list_display = ('name', 'pub_date', 'creator')
    list_filter = ('name', 'pub_date', 'creator', 'role')
    search_fields = ['creator__username', 'name', 'role']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'creator', 'role',
                                             'description', 'image', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(EarthGeoDataActor, EarthGeoDataActorAdmin)


class EarthGeoDataPatrimonyAdmin(EarthGeoDataAbstractAdmin):
    """EarthGeoDataPatrimony administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator', 'unesco')
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator',
                   'inauguration_date', 'architects', 'techniques', 'unesco', 'actor')
    search_fields = ['creator__username', 'name', 'techniques', 'architects', 'actor']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'inauguration_date', 'creator',
                                             'credit_creator', 'architects',
                                             'techniques', 'actor', 'unesco',
                                             'description', 'image', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(EarthGeoDataPatrimony, EarthGeoDataPatrimonyAdmin)


class EarthGeoDataMeetingAdmin(EarthGeoDataAbstractAdmin):
    """EarthGeoDataMeeting administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator',
                    'meeting_type', 'beginning_date', 'end_date', )
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator',
                   'meeting_type', 'beginning_date', 'end_date', 'actor')
    search_fields = ['creator__username', 'name', 'meeting_type', 'actor']
    date_hierarchy = 'beginning_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'meeting_type', 'pub_date',
                                             'beginning_date', 'end_date',
                                             'creator', 'credit_creator', 'actor',
                                             'description', 'image', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(EarthGeoDataMeeting, EarthGeoDataMeetingAdmin)


class EarthGeoDataConstructionAdmin(EarthGeoDataAbstractAdmin):
    """EarthGeoDataConstruction administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator',
                    'participative', )
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator',
                   'participative', 'inauguration_date', 'techniques', 'actor')
    search_fields = ['creator__username', 'name', 'techniques', 'actor']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date', 'creator',
                                             'credit_creator', 'actor', 'participative',
                                             'techniques', 'description',
                                             'image', 'url', 'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(EarthGeoDataConstruction, EarthGeoDataConstructionAdmin)
