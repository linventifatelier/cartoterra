"""Geodata administration interface."""
from django.contrib.gis import admin
from olwidget.admin import GeoModelAdmin
from models import EarthTechnique, EarthArchitect, \
     EarthGeoDataMeeting, EarthGeoDataPatrimony, \
     EarthGeoDataConstruction, Book
from django.conf import settings
#from stdimage import StdImageField
from imagewidget import AdminImageWidget
from forms import EarthGeoDataAbstractForm
#from sorl.thumbnail.admin import AdminImageMixin
#from sorl.thumbnail import get_thumbnail
#from widget import AdminImageFieldWithThumbWidget

#ADMIN_THUMBS_SIZE = '60x60'
#from nani import admin
from nani import admin as naniadmin

class BookAdmin(naniadmin.TranslatableAdmin):
    """InterestingLocation administration interface."""
    fieldsets = (
        ('Book Attributes', {'fields': (('isbn', ))}),
    )

admin.site.register(Book, BookAdmin)


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


class MyAdmin(admin.ModelAdmin):
    """Modified admin.ModelAdmin (include special AdminImageWidget for the
    image field)."""
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            #request = kwargs.pop("request", None)
            _request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(MyAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class MyOSMAdmin(admin.OSMGeoAdmin):
    """Modified admin.OSMGeoAdmin (include special AdminImageWidget for the
    image field). TODO: does not work."""
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            #request = kwargs.pop("request", None)
            _request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(MyOSMAdmin, self).formfield_for_dbfield(db_field,
                                                             **kwargs)


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


class EarthArchitectAdmin(admin.ModelAdmin):
    """EarthArchitect administration interface."""
    list_display = ['name', 'user']
    list_filter = ['name', 'user']
    search_fields = ['name']
    fieldsets = (
        ('Architect', {'fields': (('name', 'user'))}),
    )

admin.site.register(EarthArchitect, EarthArchitectAdmin)


#class EarthGeoDataAbstractAdmin(MyOSMAdmin):
#class EarthGeoDataAbstractAdmin(admin.OSMGeoAdmin):
class EarthGeoDataAbstractAdmin(GeoModelAdmin):
    """EarthGeoData abstract administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator')
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator')
    search_fields = ['creator__username', 'name']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'creator',
                                             'credit_creator',
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


class EarthGeoDataPatrimonyAdmin(EarthGeoDataAbstractAdmin):
    """EarthGeoDataPatrimony administration interface."""
    list_display = ('name', 'pub_date', 'creator', 'credit_creator', 'unesco')
    list_filter = ('name', 'pub_date', 'creator', 'credit_creator',
                   'inauguration_date', 'architects', 'techniques', 'unesco')
    search_fields = ['creator__username', 'name', 'techniques', 'architects']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'inauguration_date', 'creator',
                                             'credit_creator', 'architects',
                                             'techniques', 'unesco',
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
                   'meeting_type', 'beginning_date', 'end_date', )
    search_fields = ['creator__username', 'name', 'meeting_type']
    date_hierarchy = 'beginning_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'meeting_type', 'pub_date',
                                             'beginning_date', 'end_date',
                                             'creator', 'credit_creator',
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
                   'participative', 'inauguration_date', 'techniques', )
    search_fields = ['creator__username', 'name', 'techniques']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date', 'creator',
                                             'credit_creator', 'participative',
                                             'techniques', 'description',
                                             'image', 'url', 'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )

admin.site.register(EarthGeoDataConstruction, EarthGeoDataConstructionAdmin)
