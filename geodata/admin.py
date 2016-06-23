"""Geodata administration interface."""
from models import Building, Worksite, Event, Stakeholder, Image, \
    EventType, EarthTechnique, EarthRole, Profile, BuildingClassification, \
    BuildingUse, BuildingPropertyStatus, BuildingProtectionStatus, \
    EarthQuantity, BuildingHeritageStatus, EarthGroup
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericTabularInline
from imagewidget import AdminImageWidget
from hvad import admin as hvadadmin
from imagekit.admin import AdminThumbnail
from leaflet.admin import LeafletGeoAdmin
from pagedown.widgets import AdminPagedownWidget
from import_export.admin import ImportExportMixin
from resources import BuildingResource, WorksiteResource, EventResource, \
    StakeholderResource


class EarthAdmin(admin.ModelAdmin):
    """Modified admin.ModelAdmin (include special AdminImageWidget for the
    image field)."""
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(EarthAdmin, self).formfield_for_dbfield(db_field,
                                                             **kwargs)


class EarthRoleAdmin(hvadadmin.TranslatableAdmin):
    """EarthRole administration interface."""
    # list_display = ['name']
    # list_filter = ['name']
    # search_fields = ['name']

    fieldsets = (
        # ('Roles', {'fields': (('name', ))}),
        # ('Techniques', {'fields': (('name', 'description', 'image', 'url'))})
    )

admin.site.register(EarthRole, EarthRoleAdmin)


class EarthTechniqueAdmin(admin.ModelAdmin):
    """EarthTechnique administration interface."""
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

    fieldsets = (
        ('Techniques', {'fields': (('name', 'description', 'url'))}),
    )

admin.site.register(EarthTechnique, EarthTechniqueAdmin)


class EventTypeAdmin(hvadadmin.TranslatableAdmin):
    """EarthEventType administration interface."""
    # list_display = ['ident_name']
    # list_filter = ['ident_name']
    # search_fields = ['name']

    fieldsets = (
        # ('Identification Name', {'fields': (('ident_name', ))}),
        # ('Techniques', {'fields': (('name', 'description', 'image', 'url'))})
    )

admin.site.register(EventType, EventTypeAdmin)


class ImageInline(GenericTabularInline):
    model = Image
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    readonly_fields = ('admin_thumbnail', )


class GeoDataAbstractAdmin(LeafletGeoAdmin):
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
    # scrollable = False
    # map_width = 700
    # map_height = 325
    # if settings.OPENLAYERS:
    #     openlayers_url = settings.OPENLAYERS

    class Meta:
        """Abstract class."""
        abstract = True


admin.site.register(BuildingHeritageStatus, admin.ModelAdmin)
admin.site.register(BuildingClassification, admin.ModelAdmin)
admin.site.register(BuildingUse, admin.ModelAdmin)
admin.site.register(BuildingPropertyStatus, admin.ModelAdmin)
admin.site.register(BuildingProtectionStatus, admin.ModelAdmin)
admin.site.register(EarthQuantity, admin.ModelAdmin)


class BuildingAdmin(ImportExportMixin, GeoDataAbstractAdmin):
    """EarthGeoDataBuilding administration interface."""
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
    resource_class = BuildingResource

admin.site.register(Building, BuildingAdmin)


class WorksiteAdmin(ImportExportMixin, GeoDataAbstractAdmin):
    """EarthGeoDataWorksite administration interface."""
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
    resource_class = WorksiteResource

admin.site.register(Worksite, WorksiteAdmin)


class EventAdmin(ImportExportMixin, GeoDataAbstractAdmin):
    """EarthGeoDataEvent administration interface."""
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
                                             'end_date', 'unesco_chair',
                                             'number_of_stakeholders',
                                             'type_of_stakeholders',
                                             'creator',
                                             'credit_creator', 'stakeholder',
                                             'description', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )
    resource_class = EventResource

admin.site.register(Event, EventAdmin)


class StakeholderAdmin(ImportExportMixin, GeoDataAbstractAdmin):
    """EarthGeoDataStakeholder administration interface."""
    list_display = ('name', 'pub_date', 'creator')
    list_filter = ('name', 'pub_date', 'creator', 'role')
    search_fields = ['creator__username', 'name', 'role']
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Location Attributes', {'fields': (('name', 'pub_date',
                                             'creator', 'role',
                                             'unesco_chair',
                                             'description', 'url',
                                             'contact'))}),
        ('Editable Map View', {'fields': ('geometry', )}),
    )
    resource_class = StakeholderResource

admin.site.register(Stakeholder, StakeholderAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class EarthGroupAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EarthGroupAdminForm, self).__init__(*args, **kwargs)
        self.fields['description_markdown'].widget = AdminPagedownWidget()
        #self.fields['image'].widget = AdminImageWidget()


class EarthGroupAdmin(admin.ModelAdmin):
    form = EarthGroupAdminForm
    inlines = [ImageInline]


admin.site.register(EarthGroup, EarthGroupAdmin)
