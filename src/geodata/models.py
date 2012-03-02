"""GeoData methods."""
from django.contrib.gis.db import models
#from django.conf import settings
#from profiles.models import Profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta, date
#from stdimage import StdImageField
#from image import AutoImageField
#import os
#from sorl.thumbnail import ImageField, ImageWithThumbnailsField
#from sorl.thumbnail import ImageField, get_thumbnail
from sorl.thumbnail import ImageField
from nani.models import TranslatableModel,TranslatedFields


#class ProductImage(models.Model):
#    fullsize=models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT,
#    "img/fullsize"))
#    display=AutoImageField(upload_to=os.path.join(settings.MEDIA_ROOT,
#    "img/display"),prepopulate_from='fullsize', size=(300, 300))
#    thumbnail=AutoImageField(upload_to=os.path.join(settings.MEDIA_ROOT,
#    "img/thumbnail"),null=True,default='/media/noimage.jpg')

#from image import ProductImage

class Book(TranslatableModel):
    """Test"""
    isbn = models.CharField(max_length=17)
    translations = TranslatedFields(
        description = models.TextField()
    )

    def __unicode__(self):
        return self.isbn


class InterestingLocation(models.Model):
    """A spatial model for interesting locations."""
    name = models.CharField(max_length=50, )
    interestingness = models.IntegerField()
    geometry = models.PointField(srid=4326)  # EPSG:4236 is the spatial
                                             # reference for our data
    objects = models.GeoManager()  # so we can use spatial queryset methods

    def __unicode__(self):
        return self.name


class EarthTechnique(models.Model):
    """A model for earthbuilding techniques."""
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), blank=True, null=True)
    #image = models.TextField(_("image"), blank=True, null=True)
    #image = models.ImageField(upload_to='img/techniques', blank=True,
    #null=True)
    image = ImageField(upload_to='img/techniques', blank=True, null=True)
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
    url = models.URLField(_("website"), blank=True, null=True,
                          verify_exists=False)

    def __unicode__(self):
        return self.name


class EarthArchitect(models.Model):
    """A model for earthbuilding architect type (toto, vernacular, (...)?)."""
    name = models.CharField(_("name"), max_length=50)
    user = models.ForeignKey(User, verbose_name=_("user"), blank=True,
                             null=True)
    description = models.TextField(_("description"), blank=True, null=True)

    def __unicode__(self):
        return self.name


class EarthMeeting(models.Model):
    """A model for earthbuilding meeting type (seminar, conference, , ...)."""
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), blank=True, null=True)

    def __unicode__(self):
        return self.name

#class EarthMeetingContribution(models.Model):
#    """A model for earthbuilding meeting contribution."""
#    name = models.CharField(_("name"), max_length=50)
#    user = models.ManyToManyField(User,verbose_name=_("user"), blank=True,
#                                  null=True)
#    description = models.TextField(_("description"), blank=True, null=True)
#    def __unicode__(self): return self.name


class EarthGeoDataAbstract(models.Model):
    """An abstract spatial model for earthbuilding geodata."""
    name = models.CharField(_("name"), max_length=50)
    pub_date = models.DateTimeField(_("creation date"), default=datetime.now())
    #last_modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, verbose_name=_("creator"))
    credit_creator = models.BooleanField(_("credit creator"), default=True)
    description = models.TextField(_("description"), blank=True, null=True)
    image = ImageField(upload_to='img/geodata', blank=True, null=True)
    #image = models.TextField(_("image"), blank=True, null=True)
    url = models.URLField(_("website"), blank=True, null=True,
                          verify_exists=False)
    contact = models.TextField(_("contact"), blank=True, null=True)
    geometry = models.PointField(srid=4326)  # EPSG:4236 is the spatial
                                             # reference for our data
    objects = models.GeoManager()  # so we can use spatial queryset methods

    class Meta:
        """Abstract class, sorted by name."""
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name


class EarthGeoDataPatrimony(EarthGeoDataAbstract):
    """A spatial model for earthbuilding patrimony geodata."""
    classurl = "patrimony"
    architects = models.ManyToManyField(EarthArchitect,
                                        verbose_name=_("architects"),
                                        blank=True, null=True)
    techniques = models.ManyToManyField(EarthTechnique,
                                        verbose_name=_("techniques"),
                                        blank=True, null=True)
    unesco = models.BooleanField(_("unesco"), default=False)
    inauguration_date = models.DateField(_("inauguration date"),
                                         blank=True, null=True)

    def contemporary_status(self):
        """Returns the contemporary status of a meeting."""
        return self.inauguration_date <= date.today() + timedelta(days=3650)


class EarthGeoDataMeeting(EarthGeoDataAbstract):
    """A spatial model for earthbuilding patrimony geodata."""
    classurl = "meeting"
    meeting = models.ForeignKey(EarthMeeting, verbose_name=_("meeting"))
    beginning_date = models.DateField(_("beginning date"),
                                      default=date.today())
    end_date = models.DateField(_("end date"), default=date.today())
    ## techniques = models.ManyToManyField(EarthTechnique,
    ##                                     verbose_name=_("techniques"),
    ##                                     blank=True, null=True)

    ## contributions = models.ManyToManyField(EarthMeetingContribution,
    ##                                        verbose_name=_("contributions"),
    ##                                        blank=True, null=True)

    def ended_status(self):
        """Says if a meeting is ended or not."""
        return self.beginning_date <= date.today()


class EarthGeoDataConstruction(EarthGeoDataAbstract):
    """A spatial model for earthbuilding construction geodata."""
    classurl = "construction"
    participative = models.BooleanField(_("participative"), default=False)
    techniques = models.ManyToManyField(EarthTechnique,
                                        verbose_name=_("techniques"),
                                        blank=True, null=True)

