from django.contrib.gis.db import models
from profiles.models import Profile
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class InterestingLocation(models.Model):
    """A spatial model for interesting locations """
    name = models.CharField(max_length=50, )
    interestingness = models.IntegerField() 
    geometry = models.PointField(srid=4326) #EPSG:4236 is the spatial reference for our data
    objects = models.GeoManager() # so we can use spatial queryset methods

    def __unicode__(self): return self.name 

class EarthGeoData(models.Model):
    """A spatial model for earthbuilding geodata """
    name = models.CharField(_("name"), max_length=50)
    pub_date = models.DateTimeField(_("creation date"))
    creator = models.ForeignKey(Profile)
    creator.short_description = _("crea")
    description = models.TextField(_("description"),blank=True)
    image = models.TextField(_("image"),blank=True)
    url = models.URLField(_("website"),blank=True, verify_exists=False)
    contact = models.TextField(_("contact"),blank=True)
    interestingness = models.IntegerField(_("interestingness"),blank=True)
    geometry = models.PointField(srid=4326) #EPSG:4236 is the spatial reference for our data
    objects = models.GeoManager() # so we can use spatial queryset methods

    def __unicode__(self): return self.name 
