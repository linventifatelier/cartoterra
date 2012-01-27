from django.contrib.gis.db import models
#from profiles.models import Profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta, date

# Create your models here.

class InterestingLocation(models.Model):
    """A spatial model for interesting locations """
    name = models.CharField(max_length=50, )
    interestingness = models.IntegerField() 
    geometry = models.PointField(srid=4326) #EPSG:4236 is the spatial reference for our data
    objects = models.GeoManager() # so we can use spatial queryset methods

    def __unicode__(self): return self.name 


class EarthTechnique(models.Model):
    """A model for earthbuilding techniques."""
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"),blank=True,null=True)
    image = models.TextField(_("image"),blank=True,null=True)
    url = models.URLField(_("website"),blank=True,null=True,verify_exists=False)
    
    def __unicode__(self): return self.name 


class EarthArchitect(models.Model):
    """A model for earthbuilding architect type (toto, tata, vernacular, (...)?)."""
    name = models.CharField(_("name"), max_length=50)
    user = models.ForeignKey(User,verbose_name=_("user"),blank=True,null=True)
    description = models.TextField(_("description"),blank=True,null=True)
    
    def __unicode__(self): return self.name 


class EarthMeeting(models.Model):
    """A model for earthbuilding meeting type (seminar, conference, , ...)."""
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"),blank=True,null=True)

    def __unicode__(self): return self.name 

#class EarthMeetingContribution(models.Model):
#    """A model for earthbuilding meeting contribution."""
#    name = models.CharField(_("name"), max_length=50)
#    user = models.ManyToManyField(User,verbose_name=_("user"),blank=True,null=True)
#    description = models.TextField(_("description"),blank=True,null=True)
#    def __unicode__(self): return self.name 


class EarthGeoDataAbstract(models.Model):
    """An abstract spatial model for earthbuilding geodata."""
    name = models.CharField(_("name"), max_length=50)
    pub_date = models.DateTimeField(_("creation date"),default=datetime.now())
    creator = models.ForeignKey(User,verbose_name=_("creator"))
    description = models.TextField(_("description"),blank=True,null=True)
    image = models.TextField(_("image"),blank=True,null=True)
    url = models.URLField(_("website"),blank=True,null=True,verify_exists=False)
    contact = models.TextField(_("contact"),blank=True,null=True)
    geometry = models.PointField(srid=4326) #EPSG:4236 is the spatial reference for our data
    objects = models.GeoManager() # so we can use spatial queryset methods
    class Meta:
            abstract = True
            ordering = ['name']

    def __unicode__(self): return self.name 


class EarthGeoDataPatrimony(EarthGeoDataAbstract):
    """A spatial model for earthbuilding patrimony geodata."""
    architects = models.ManyToManyField(EarthArchitect,verbose_name=_("architects"),blank=True,null=True)
    techniques = models.ManyToManyField(EarthTechnique,verbose_name=_("techniques"),blank=True,null=True)
    unesco = models.BooleanField(_("unesco"),default=False)
    inauguration_date = models.DateField(_("inauguration date"),blank=True,null=True)
    def contemporary_status(self):
        """Returns the contemporary status of a meeting."""
        return self.inauguration_date <= date.today() + timedelta(days=3650)


class EarthGeoDataMeeting(EarthGeoDataAbstract):
    """A spatial model for earthbuilding patrimony geodata."""
    meeting = models.ForeignKey(EarthMeeting,verbose_name=_("meeting"))
    beginning_date = models.DateField(_("beginning date"),default=date.today())
    end_date = models.DateField(_("end date"),default=date.today())
    #techniques = models.ManyToManyField(EarthTechnique,verbose_name=_("techniques"),blank=True,null=True)

    #contributions = models.ManyToManyField(EarthMeetingContribution,verbose_name=_("contributions"),blank=True,null=True)
    
    def ended_status(self):
        """Says if a meeting is ended or not."""
        return self.beginning_date <= date.today()

class EarthGeoDataConstruction(EarthGeoDataAbstract):
    """A spatial model for earthbuilding construction geodata."""
    participative = models.BooleanField(_("participative"),default=False)
    techniques = models.ManyToManyField(EarthTechnique,verbose_name=_("techniques"),blank=True,null=True)
