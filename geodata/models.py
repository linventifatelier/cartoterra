"""GeoData methods."""
from django.contrib.gis.db import models
#from django.conf import settings
#from profiles.models import Profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta, date
from django.utils.timezone import now
#from stdimage import StdImageField
#from image import AutoImageField
#import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from hvad.models import TranslatableModel, TranslatedFields
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


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


#class EarthArchitect(models.Model):
#    """A model for earthbuilding architect type (toto, vernacular, (...)?)."""
#    name = models.CharField(_("name"), max_length=50)
#    user = models.ForeignKey(User, verbose_name=_("user"), blank=True,
#                             null=True)
#    description = models.TextField(_("description"), blank=True, null=True)
#
#    def get_model(self):
#        return EarthArchitect
#
#    def __unicode__(self):
#        return self.name


class Image(models.Model):
    #image = ImageField(upload_to='img/geodata', blank=True, null=True)
    original = models.ImageField(upload_to='img/geodata')
    legend = models.CharField(_("legend"), max_length=50, blank=True,
                              null=True)
    image = ImageSpecField(image_field='original',
                           processors=[ResizeToFill(300, 300)],
                           format='JPEG',
                           options={'quality': 80})
    thumbnail = ImageSpecField(image_field='original',
                               processors=[ResizeToFill(100, 100)],
                               format='JPEG',
                               options={'quality': 60})
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

#    class Meta:
#        """Abstract class."""
#        abstract = True


class EarthGeoDataAbstract(models.Model):
    """An abstract spatial model for earthbuilding geodata."""
    name = models.CharField(_("name"), max_length=50)
    pub_date = models.DateTimeField(_("creation date"), default=now())
    creator = models.ForeignKey(User, verbose_name=_("creator"))
    description = models.TextField(_("description"), blank=True, null=True)
    #image = ImageField(upload_to='img/geodata', blank=True, null=True)
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
    """Actor role"""
    #name = models.CharField(_("name"), max_length=50)
    ident_name = models.CharField(_("Identification name"), max_length=255,
                                  unique=True)

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


class EarthGeoDataActor(EarthGeoDataAbstract):
    """A spatial model for earthbuilding actors."""
    role = models.ManyToManyField(EarthRole,
                                  verbose_name=_("role"),
                                  blank=True, null=True)

    class Meta:
        verbose_name = _("actor")
        verbose_name_plural = _("actors")

    @models.permalink
    def get_absolute_url(self):
        return ("show_actor", [self.id])


#class ActorImage(AbstractImage):
#    geodata = models.ForeignKey(EarthGeoDataActor, related_name='image')


class EarthGeoDataPatrimony(EarthGeoDataAbstract):
    """A spatial model for earthbuilding patrimony geodata."""
    #architects = models.ManyToManyField(EarthArchitect,
    #                                    verbose_name=_("architects"),
    #                                    blank=True, null=True)
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    architects = models.TextField(_("architects"), blank=True, null=True)
    techniques = models.ManyToManyField(EarthTechnique,
                                        verbose_name=_("techniques"),
                                        blank=True, null=True)
    unesco = models.BooleanField(_("unesco"), default=False)
    inauguration_date = models.DateField(_("inauguration date"),
                                         blank=True, null=True)
    actor = models.ManyToManyField(EarthGeoDataActor,
                                   verbose_name=_("actor"),
                                   blank=True, null=True)

    class Meta:
        verbose_name = _("patrimony")
        verbose_name_plural = _("patrimonies")

    def get_model(self):
        return EarthGeoDataPatrimony

    @models.permalink
    def get_absolute_url(self):
        return ("show_patrimony", [self.id])

    def contemporary_status(self):
        """Returns the contemporary status of a meeting."""
        return self.inauguration_date <= date.today() + timedelta(days=3650)


class EarthMeetingType(TranslatableModel):
    """Meeting type"""
    #name = models.CharField(_("name"), max_length=50)
    ident_name = models.CharField(_("Identification name"), max_length=255,
                                  unique=True)

    translations = TranslatedFields(
        name=models.CharField(_("Translated name"), max_length=255, blank=True,
                              null=True)
    )

    def get_model(self):
        return EarthMeetingType

    def __unicode__(self):
        return self.ident_name
        #return self.lazy_translation_getter('name', self.name)
        #return str(self.safe_translation_getter('name'))
        #return str(self.id)


class EarthGeoDataConstruction(EarthGeoDataAbstract):
    """A spatial model for earthbuilding construction geodata."""
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    participative = models.BooleanField(_("participative"), default=False)
    techniques = models.ManyToManyField(EarthTechnique,
                                        verbose_name=_("techniques"),
                                        blank=True, null=True)
    inauguration_date = models.DateField(_("inauguration date"),
                                         blank=True, null=True)
    actor = models.ManyToManyField(EarthGeoDataActor,
                                   verbose_name=_("actor"),
                                   blank=True, null=True)

    class Meta:
        verbose_name = _("construction")
        verbose_name_plural = _("constructions")

    def get_model(self):
        return EarthGeoDataConstruction

    @models.permalink
    def get_absolute_url(self):
        return ("show_construction", [self.id])


class EarthGeoDataMeeting(EarthGeoDataAbstract):
    """A spatial model for earthbuilding patrimony geodata."""
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    meeting_type = models.ForeignKey(EarthMeetingType,
                                     verbose_name=_("meeting type"),
                                     blank=True, null=True)
    beginning_date = models.DateField(_("beginning date"),
                                      default=date.today())
    end_date = models.DateField(_("end date"), default=date.today())
    actor = models.ManyToManyField(EarthGeoDataActor,
                                   verbose_name=_("actor"),
                                   blank=True, null=True)

    class Meta:
        verbose_name = _("meeting")
        verbose_name_plural = _("meetings")

    def get_model(self):
        return EarthGeoDataMeeting

    @models.permalink
    def get_absolute_url(self):
        return ("show_meeting", [self.id])

    def ended_status(self):
        """Says if a meeting is ended or not."""
        return self.beginning_date <= date.today()
