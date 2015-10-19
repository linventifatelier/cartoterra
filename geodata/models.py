"""GeoData models."""
from django.contrib.gis.db import models
#from django.conf import settings
#from profiles.models import Profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta, date
from django.utils.timezone import now
#from image import AutoImageField
#import os
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit
from hvad.models import TranslatableModel, TranslatedFields
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.validators import RegexValidator
import re
from django.db.models.signals import post_save


ident_regex = re.compile(r'^[a-zA-Z0-9_\-]+$')


class EarthTechnique(models.Model):
    """A model for earthbuilding techniques."""
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), blank=True, null=True)
    #image = models.TextField(_("image"), blank=True, null=True)
    #image = models.ImageField(upload_to='img/techniques', blank=True,
    #null=True)
    ### image = ImageField(upload_to='img/techniques', blank=True, null=True)
    #image = ImageWithThumbnailsField(upload_to='img/techniques',
    #thumbnail={'size': (200, 200)}, blank=True, null=True)
    #image = ImageField(upload_to='img/techniques', thumbnail={'size': (200,
    #200)}, blank=True, null=True)

    #image_display = AutoImageField(upload_to='img/techniques/display',
    #prepopulate_from='image', size=(300, 300), blank=True, null=True)
    #image = StdImageField(upload_to='img/techniques', size=(640, 640),
    #thumbnail_size=(100, 100), blank=True, null=True)
    #image_display = AutoImageField(upload_to='img/techniques/display',
    #prepopulate_from='image', size=(640, 640), blank=True, null=True)
    #fullsize = models.ImageField(upload_to=os.path.join(MEDIA_ROOT,
    #"img/technique/fullsize"))
    #display = AutoImageField(upload_to=os.path.join(MEDIA_ROOT,
    #"img/technique/display"),prepopulate_from='fullsize', size=(300, 300))
    url = models.URLField(_("website"), blank=True, null=True)

    def get_model(self):
        return EarthTechnique

    def __unicode__(self):
        return self.name


class Image(models.Model):
    #image = ImageField(upload_to='img/geodata', blank=True, null=True)
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
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["id"]


class GeoDataAbstract(models.Model):
    """An abstract spatial model for earthbuilding geodata."""
    name = models.CharField(_("name"), max_length=100)
    pub_date = models.DateTimeField(_("creation date"), default=now())
    creator = models.ForeignKey(User, verbose_name=_("creator"))
    description = models.TextField(_("description"), blank=True, null=True)
    image = generic.GenericRelation(Image)
    url = models.URLField(_("website"), blank=True, null=True)
    contact = models.TextField(_("contact"), blank=True, null=True)
    geometry = models.PointField(srid=4326, blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        """Abstract class, sorted by name."""
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name


class EarthRole(TranslatableModel):
    """Stakeholder role"""
    #name = models.CharField(_("name"), max_length=50)
    ident_name = models.CharField(_("Identification name"), max_length=50,
                                  unique=True,
                                  validators=[
                                      RegexValidator(regex=ident_regex)
                                  ])

    translations = TranslatedFields(
        name=models.CharField(_("Translated name"), max_length=255,
                              blank=True, null=True)
    )

    def get_model(self):
        return EarthRole

    def __unicode__(self):
        return self.ident_name
        #return self.lazy_translation_getter('name', self.name)
        #return str(self.safe_translation_getter('name'))
        #return str(self.id)


class Stakeholder(GeoDataAbstract):
    """A spatial model for stakeholders."""
    role = models.ManyToManyField(EarthRole,
                                  verbose_name=_("role"),
                                  blank=True, null=True)
    unesco_chair = models.BooleanField(_("UNESCO Chair Earthen Architecture"),
                                       default=False)

    class Meta:
        verbose_name = _("stakeholder")

    @models.permalink
    def get_absolute_url(self):
        return ("show_stakeholder", [self.id])


class Building(GeoDataAbstract):
    """A spatial model for building geodata."""
    #architects = models.ManyToManyField(EarthArchitect,
    #                                    verbose_name=_("architects"),
    #                                    blank=True, null=True)
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    architects = models.TextField(_("architects"), blank=True, null=True)
    techniques = models.ManyToManyField(EarthTechnique,
                                        verbose_name=_("techniques"),
                                        blank=True, null=True)
    unesco = models.BooleanField(_("world heritage"), default=False)
    inauguration_date = models.DateField(_("inauguration date"),
                                         blank=True, null=True)
    stakeholder = models.ManyToManyField(Stakeholder,
                                         verbose_name=_("stakeholder"),
                                         blank=True, null=True)

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
    #name = models.CharField(_("name"), max_length=50)
    ident_name = models.CharField(_("Identification name"), max_length=50,
                                  unique=True,
                                  validators=[
                                      RegexValidator(regex=ident_regex)
                                  ])

    translations = TranslatedFields(
        name=models.CharField(_("Translated name"), max_length=255, blank=True,
                              null=True)
    )

    def get_model(self):
        return EventType

    def __unicode__(self):
        return self.ident_name
        #return self.lazy_translation_getter('name', self.name)
        #return str(self.safe_translation_getter('name'))
        #return str(self.id)


class Worksite(GeoDataAbstract):
    """A spatial model for worksite geodata."""
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    participative = models.BooleanField(_("participative"), default=False)
    techniques = models.ManyToManyField(EarthTechnique,
                                        verbose_name=_("techniques"),
                                        blank=True, null=True)
    inauguration_date = models.DateField(_("inauguration date"),
                                         blank=True, null=True)
    stakeholder = models.ManyToManyField(Stakeholder,
                                         verbose_name=_("stakeholder"),
                                         blank=True, null=True)

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
    beginning_date = models.DateField(_("beginning date"),
                                      default=date.today())
    end_date = models.DateField(_("end date"), default=date.today())
    number_of_stakeholders = models.PositiveIntegerField(
        _("Number of stakeholders"), blank=True,
        null=True)
    type_of_stakeholders = models.ManyToManyField(
        EarthRole, verbose_name=_("Type of stakeholders"), blank=True,
        null=True)
    stakeholder = models.ManyToManyField(Stakeholder,
                                         verbose_name=_("stakeholder"),
                                         blank=True, null=True)

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


class Profile(models.Model):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'))
    #about = models.TextField(_("about"), null=True, blank=True)
    #location = models.CharField(_("location"), max_length=40, null=True,
    #                            blank=True)
    #website = models.URLField(_("website"), null=True, blank=True,
    #                          verify_exists=False)
    r_building = models.ManyToManyField(
        Building,
        verbose_name=_("building recommendations"),
        related_name="recommended_by",
        null=True, blank=True)
    r_worksite = models.ManyToManyField(
        Worksite,
        verbose_name=_("worksite recommendations"),
        related_name="recommended_by",
        null=True, blank=True)
    r_event = models.ManyToManyField(
        Event,
        verbose_name=_("event recommendations"),
        related_name="recommended_by",
        null=True, blank=True)
    r_stakeholder = models.ManyToManyField(
        Stakeholder,
        verbose_name=_("stakeholder recommendations"),
        related_name="recommended_by",
        null=True, blank=True)

    class Meta:
        permissions = (
            ("world_heritage", _("Can modify world heritage properties")),
            ("unesco_chair",
             _("Can modify UNESCO Chair Earthen Architecture")),
        )

    def recommends(self, geodata):
        if isinstance(geodata, Building):
            return self.r_building.filter(id=geodata.id).exists()
        elif isinstance(geodata, Worksite):
            return self.r_worksite.filter(id=geodata.id).exists()
        elif isinstance(geodata, Event):
            return self.r_event.filter(id=geodata.id).exists()
        elif isinstance(geodata, Stakeholder):
            return self.r_stakeholder.filter(id=geodata.id).exists()
        else:
            return False


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
