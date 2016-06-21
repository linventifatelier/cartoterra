from models import Building, Worksite, Event, Stakeholder, Image, \
    EventType, EarthTechnique, EarthRole, Profile, BuildingClassification, \
    BuildingUse, BuildingPropertyStatus, BuildingProtectionStatus, \
    EarthQuantity, BuildingHeritageStatus
from django.contrib.auth.models import User
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class GeodataResource(resources.ModelResource):
    geometry = fields.Field()
    creator = fields.Field(
        column_name='creator',
        attribute='creator',
        widget=ForeignKeyWidget(User, 'username')
    )
    techniques = fields.Field(
        column_name='techniques',
        attribute='techniques',
        widget=ForeignKeyWidget(EarthTechnique, 'name')
    )

    def dehydrate_geometry(self, geodata):
        # longitude latitude in srid=4326
        return '%s %s' % geodata.geometry.tuple

    class Meta:
        skip_unchanged = True
        report_skipped = True


class BuildingResource(GeodataResource):
    class Meta:
        model = Building


class WorksiteResource(GeodataResource):
    class Meta:
        model = Worksite


class EventResource(GeodataResource):
    class Meta:
        model = Event


class StakeholderResource(GeodataResource):
    class Meta:
        model = Stakeholder
