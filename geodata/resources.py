from models import Building, Worksite, Event, Stakeholder, \
    EventType, EarthTechnique, EarthRole, BuildingClassification, \
    BuildingUse, BuildingPropertyStatus, BuildingProtectionStatus, \
    EarthQuantity, BuildingHeritageStatus, EarthGroup
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget, Widget


class GeometryWidget(Widget):
    def clean(self, value):
        if not value:
            return None
        val = value
        srid = 4326
        if ":" in value:
            sridcoords = value.split(':')
            srid_s = sridcoords[0]
            srid = int(srid_s)
            val = sridcoords[1]
        coords_s = val.split(',')
        coords = [float(x) for x in coords_s]
        return Point(coords[0], coords[1], srid=srid)

    def render(self, geometry):
        if geometry:
            # longitude latitude in srid=4326
            return '%s:%s,%s' % \
                (geometry.srid, geometry.coords[0], geometry.coords[1])
        else:
            return None


class GeodataResource(resources.ModelResource):
    geometry = fields.Field(
        column_name='geometry',
        attribute='geometry',
        widget=GeometryWidget()
    )
    creator = fields.Field(
        column_name='creator',
        attribute='creator',
        widget=ForeignKeyWidget(User, 'username')
    )
    techniques = fields.Field(
        column_name='techniques',
        attribute='techniques',
        widget=ManyToManyWidget(model=EarthTechnique, field='name')
    )
    groups = fields.Field(
        column_name='groups',
        attribute='earthgroup_set',
        widget=ManyToManyWidget(model=EarthGroup, field='name')
    )

    class Meta:
        skip_unchanged = True
        report_skipped = True


class BuildingResource(GeodataResource):
    classification = fields.Field(
        column_name='classification',
        attribute='classification',
        widget=ForeignKeyWidget(BuildingClassification, 'name')
    )
    use = fields.Field(
        column_name='use',
        attribute='use',
        widget=ForeignKeyWidget(BuildingUse, 'name')
    )
    property_status = fields.Field(
        column_name='property_status',
        attribute='property_status',
        widget=ForeignKeyWidget(BuildingPropertyStatus, 'name')
    )
    earth_quantity = fields.Field(
        column_name='earth_quantity',
        attribute='earth_quantity',
        widget=ForeignKeyWidget(EarthQuantity, 'quantity')
    )
    protection_status = fields.Field(
        column_name='protection_status',
        attribute='protection_status',
        widget=ForeignKeyWidget(BuildingProtectionStatus, 'name')
    )
    heritage_status = fields.Field(
        column_name='heritage_status',
        attribute='heritage_status',
        widget=ForeignKeyWidget(BuildingHeritageStatus, 'name')
    )
    stakeholder = fields.Field(
        column_name='stakeholder',
        attribute='stakeholder',
        widget=ManyToManyWidget(model=Stakeholder, field='name')
    )

    class Meta:
        model = Building


class WorksiteResource(GeodataResource):
    stakeholder = fields.Field(
        column_name='stakeholder',
        attribute='stakeholder',
        widget=ManyToManyWidget(model=Stakeholder, field='name')
    )

    class Meta:
        model = Worksite


class EventResource(GeodataResource):
    event_type = fields.Field(
        column_name='event_type',
        attribute='event_type',
        widget=ForeignKeyWidget(EventType, 'ident_name')
    )
    type_of_stakeholders = fields.Field(
        column_name='type_of_stakeholders',
        attribute='type_of_stakeholders',
        widget=ManyToManyWidget(model=EarthRole, field='ident_name')
    )
    stakeholder = fields.Field(
        column_name='stakeholder',
        attribute='stakeholder',
        widget=ManyToManyWidget(model=Stakeholder, field='name')
    )

    class Meta:
        model = Event


class StakeholderResource(GeodataResource):
    role = fields.Field(
        column_name='role',
        attribute='role',
        widget=ManyToManyWidget(model=EarthRole, field='ident_name')
    )

    class Meta:
        model = Stakeholder
