"""GeoData models."""
from django.contrib.gis.db import models
# from django.conf import settings
# from profiles.models import Profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta, date
from django.utils.timezone import now
# from image import AutoImageField
# import os
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit
from hvad.models import TranslatableModel, TranslatedFields
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.core.validators import RegexValidator
import re
import markdown
from django.db.models.signals import post_save


ident_regex = re.compile(r'^[a-zA-Z0-9_\-]+$')


def today(datetime):
    datetime().date()


class EarthTechnique(models.Model):
    """A model for earthbuilding techniques."""
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), blank=True, null=True)
    # image = models.TextField(_("image"), blank=True, null=True)
    # image = models.ImageField(upload_to='img/techniques', blank=True,
    # null=True)
    # ## image = ImageField(upload_to='img/techniques', blank=True, null=True)
    # image = ImageWithThumbnailsField(upload_to='img/techniques',
    # thumbnail={'size': (200, 200)}, blank=True, null=True)
    # image = ImageField(upload_to='img/techniques', thumbnail={'size': (200,
    # 200)}, blank=True, null=True)

    # image_display = AutoImageField(upload_to='img/techniques/display',
    # prepopulate_from='image', size=(300, 300), blank=True, null=True)
    # image = StdImageField(upload_to='img/techniques', size=(640, 640),
    # thumbnail_size=(100, 100), blank=True, null=True)
    # image_display = AutoImageField(upload_to='img/techniques/display',
    # prepopulate_from='image', size=(640, 640), blank=True, null=True)
    # fullsize = models.ImageField(upload_to=os.path.join(MEDIA_ROOT,
    # "img/technique/fullsize"))
    # display = AutoImageField(upload_to=os.path.join(MEDIA_ROOT,
    # "img/technique/display"),prepopulate_from='fullsize', size=(300, 300))
    url = models.URLField(_("website"), blank=True, null=True)

    def get_model(self):
        return EarthTechnique

    def __unicode__(self):
        return self.name


class Image(models.Model):
    # image = ImageField(upload_to='img/geodata', blank=True, null=True)
    original = models.ImageField(upload_to='img/geodata')
    display = ImageSpecField(source='original',
                             processors=[ResizeToFit(800, 800)],
                             format='JPEG',
                             options={'quality': 80})
    legend = models.CharField(_("caption"), max_length=100, blank=True,
                              null=True)
    image = ImageSpecField(source='original',
                           processors=[ResizeToFill(300, 300)],
                           format='JPEG',
                           options={'quality': 80})
    thumbnail = ImageSpecField(source='original',
                               processors=[ResizeToFill(100, 100)],
                               format='JPEG',
                               options={'quality': 60})
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["id"]


class GeoDataAbstract(models.Model):
    """An abstract spatial model for earthbuilding geodata."""
    name = models.CharField(_("name"), max_length=100)
    pub_date = models.DateTimeField(_("creation date"), default=now)
    creator = models.ForeignKey(User, verbose_name=_("creator"))
    description = models.TextField(_("description"), blank=True, null=True)
    image = fields.GenericRelation(Image)
    url = models.URLField(_("website"), blank=True, null=True)
    contact = models.TextField(_("contact"), blank=True, null=True)
    geometry = models.PointField(srid=4326, blank=True, null=True)
    objects = models.GeoManager()
    techniques = models.ManyToManyField(EarthTechnique,
                                        verbose_name=_("techniques"),
                                        blank=True)

    class Meta:
        """Abstract class, sorted by name."""
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name


class EarthRole(TranslatableModel):
    """Stakeholder role"""
    # name = models.CharField(_("name"), max_length=50)
    ident_name = models.CharField(
        _("Identification name"), max_length=50, unique=True,
        validators=[RegexValidator(regex=ident_regex)]
    )

    translations = TranslatedFields(
        name=models.CharField(_("Translated name"), max_length=255,
                              blank=True, null=True)
    )

    def get_model(self):
        return EarthRole

    def __unicode__(self):
        return self.ident_name
        # return self.lazy_translation_getter('name', self.name)
        # return str(self.safe_translation_getter('name'))
        # return str(self.id)


class Stakeholder(GeoDataAbstract):
    """A spatial model for stakeholders."""
    role = models.ManyToManyField(EarthRole,
                                  verbose_name=_("role"),
                                  blank=True)
    unesco_chair = models.BooleanField(_("UNESCO Chair Earthen Architecture"),
                                       default=False)
    isceah = models.BooleanField(_("ISCEAH"), default=False)

    class Meta:
        verbose_name = _("stakeholder")

    @models.permalink
    def get_absolute_url(self):
        return ("show_stakeholder", [self.id])


class BuildingHeritageStatus(models.Model):
    """A model for building heritage statuses."""
    name = models.CharField(_("name"), max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("building heritage status")
        verbose_name_plural = _("building heritage statuses")


class BuildingClassification(models.Model):
    """A model for building classifications."""
    name = models.CharField(_("name"), max_length=50)

    def __unicode__(self):
        return self.name


class BuildingUse(models.Model):
    """A model for building uses."""
    name = models.CharField(_("name"), max_length=50)

    def __unicode__(self):
        return self.name


class BuildingPropertyStatus(models.Model):
    """A model for building property status."""
    name = models.CharField(_("name"), max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("building property status")
        verbose_name_plural = _("building property statuses")


CULTURAL_LANDSCAPE_CHOICES = (
    (None, '---------'), (True, _("Yes")), (False, _("No"))
)


class BuildingProtectionStatus(models.Model):
    """A model for building protection status."""
    name = models.CharField(_("name"), max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("building protection status")
        verbose_name_plural = _("building protection statuses")


class EarthQuantity(models.Model):
    """A model for earthen material quantity."""
    quantity = models.CharField(_("quantity"), max_length=50)

    def __unicode__(self):
        return self.quantity

    class Meta:
        verbose_name = _("earthen material quantity")
        verbose_name_plural = _("earthen material quantities")


class Building(GeoDataAbstract):
    """A spatial model for building geodata."""
    detailed_description = models.TextField(
        _("detailed description"), blank=True, null=True
    )
    classification = models.ForeignKey(
        BuildingClassification, verbose_name=_("classification"),
        blank=True, null=True
    )
    use = models.ForeignKey(
        BuildingUse, verbose_name=_("use"), blank=True, null=True
    )
    property_status = models.ForeignKey(
        BuildingPropertyStatus, verbose_name=_("property status"),
        blank=True, null=True
    )
    cultural_landscape = models.NullBooleanField(
        choices=CULTURAL_LANDSCAPE_CHOICES,
        verbose_name=_("cultural landscape"), blank=True, null=True,
        default=None
    )
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    architects = models.TextField(_("architects"), blank=True, null=True)
    earth_quantity = models.ForeignKey(
        EarthQuantity,
        verbose_name=_("quantity of earthen material in the structure"),
        blank=True, null=True
    )
    condition = models.TextField(
        _("site condition and threats"), blank=True, null=True
    )
    references = models.TextField(
        _("principal references"), blank=True, null=True
    )
    unesco = models.BooleanField(_("world heritage"), default=False)
    protection_status = models.ForeignKey(
        BuildingProtectionStatus, verbose_name=_("protection status"),
        blank=True, null=True
    )
    heritage_status = models.ForeignKey(
        BuildingHeritageStatus, verbose_name=_("heritage or contemporary"),
        blank=True, null=True
    )
    isceah = models.BooleanField(_("ISCEAH"), default=False)
    inauguration_date = models.DateField(
        _("inauguration date"), blank=True, null=True
    )
    construction_date = models.CharField(
        _("Approximative construction date"), blank=True, null=True,
        max_length=50
    )
    stakeholder = models.ManyToManyField(
        Stakeholder, verbose_name=_("stakeholder"), blank=True
    )

    class Meta:
        verbose_name = _("building")
        verbose_name_plural = _("buildings")

    def get_model(self):
        return Building

    @models.permalink
    def get_absolute_url(self):
        return ("show_building", [self.id])

    def contemporary_status(self):
        """Returns the contemporary status of a building."""
        return self.inauguration_date <= date.today() + timedelta(days=3650)


class EventType(TranslatableModel):
    """Event type"""
    # name = models.CharField(_("name"), max_length=50)
    ident_name = models.CharField(
        _("Identification name"), max_length=50, unique=True,
        validators=[RegexValidator(regex=ident_regex)]
    )

    translations = TranslatedFields(
        name=models.CharField(_("Translated name"), max_length=255, blank=True,
                              null=True)
    )

    def get_model(self):
        return EventType

    def __unicode__(self):
        return self.ident_name
        # return self.lazy_translation_getter('name', self.name)
        # return str(self.safe_translation_getter('name'))
        # return str(self.id)


class Worksite(GeoDataAbstract):
    """A spatial model for worksite geodata."""
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    participative = models.BooleanField(_("participative"), default=False)
    inauguration_date = models.DateField(_("inauguration date"), blank=True)
    stakeholder = models.ManyToManyField(Stakeholder,
                                         verbose_name=_("stakeholder"),
                                         blank=True)

    class Meta:
        verbose_name = _("worksite")
        verbose_name_plural = _("worksites")

    def get_model(self):
        return Worksite

    @models.permalink
    def get_absolute_url(self):
        return ("show_worksite", [self.id])


class Event(GeoDataAbstract):
    """A spatial model for event geodata."""
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    event_type = models.ForeignKey(EventType,
                                   verbose_name=_("event type"),
                                   blank=True, null=True)
    unesco_chair = models.BooleanField(_("UNESCO Chair Earthen Architecture"),
                                       default=False)
    beginning_date = models.DateField(_("beginning date"), default=today(now))
    end_date = models.DateField(_("end date"), default=today(now))
    number_of_stakeholders = models.PositiveIntegerField(
        _("Number of stakeholders"), blank=True,
        null=True)
    type_of_stakeholders = models.ManyToManyField(
        EarthRole, verbose_name=_("Type of stakeholders"), blank=True)
    stakeholder = models.ManyToManyField(Stakeholder,
                                         verbose_name=_("stakeholder"),
                                         blank=True)

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def get_model(self):
        return Event

    @models.permalink
    def get_absolute_url(self):
        return ("show_event", [self.id])

    def ended_status(self):
        """Says if an event is ended or not."""
        return self.beginning_date <= date.today()


class EarthGroup(models.Model):
    name = models.CharField(_("name"), max_length=50)
    pub_date = models.DateTimeField(_("creation date"), default=now)
    description_markdown = models.TextField(_("description"), blank=True, null=True)
    description = models.TextField(blank=True, null=True, editable=False)
    logo = models.ImageField(upload_to='img/group')
    logo_thumbnail = ImageSpecField(source='logo',
                                    processors=[ResizeToFit(80, 80)],
                                    format='JPEG',
                                    options={'quality': 80})
    image = fields.GenericRelation(Image)
    buildings = models.ManyToManyField(Building, blank=True)
    worksites = models.ManyToManyField(Worksite, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    stakeholders = models.ManyToManyField(Stakeholder, blank=True)
    administrators = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name

    def save(self):
        self.description = markdown.markdown(self.description_markdown)
        super(EarthGroup, self).save()

    @models.permalink
    def get_absolute_url(self):
        return ("group_detail", [self.id])


class Profile(models.Model):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'))
    # about = models.TextField(_("about"), null=True, blank=True)
    # location = models.CharField(_("location"), max_length=40, null=True,
    #                             blank=True)
    # website = models.URLField(_("website"), null=True, blank=True,
    #                           verify_exists=False)
    r_building = models.ManyToManyField(
        Building,
        verbose_name=_("building recommendations"),
        related_name="recommended_by",
        blank=True)
    r_worksite = models.ManyToManyField(
        Worksite,
        verbose_name=_("worksite recommendations"),
        related_name="recommended_by",
        blank=True)
    r_event = models.ManyToManyField(
        Event,
        verbose_name=_("event recommendations"),
        related_name="recommended_by",
        blank=True)
    r_stakeholder = models.ManyToManyField(
        Stakeholder,
        verbose_name=_("stakeholder recommendations"),
        related_name="recommended_by",
        blank=True)
    r_group = models.ManyToManyField(
        EarthGroup,
        verbose_name=_("group recommendations"),
        related_name="recommended_by",
        blank=True)

    class Meta:
        permissions = (
            ("world_heritage", _("Can modify world heritage properties")),
            ("unesco_chair",
             _("Can modify UNESCO Chair Earthen Architecture")),
            ("isceah", _("Can modify ISCEAH properties")),
        )

    def recommends(self, geodata):
        if isinstance(geodata, Building):
            return self.r_building.filter(pk=geodata.pk).exists()
        elif isinstance(geodata, Worksite):
            return self.r_worksite.filter(pk=geodata.pk).exists()
        elif isinstance(geodata, Event):
            return self.r_event.filter(pk=geodata.pk).exists()
        elif isinstance(geodata, Stakeholder):
            return self.r_stakeholder.filter(pk=geodata.pk).exists()
        elif isinstance(geodata, EarthGroup):
            return self.r_group.filter(pk=geodata.pk).exists()
        else:
            return False


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
