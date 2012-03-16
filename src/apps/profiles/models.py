from django.db import models
from django.utils.translation import ugettext_lazy as _
from geodata.models import EarthGeoDataPatrimony, EarthGeoDataConstruction, \
     EarthGeoDataMeeting


from idios.models import ProfileBase


class Profile(ProfileBase):
    name = models.CharField(_("name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("about"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=40, null=True,
                                blank=True)
    website = models.URLField(_("website"), null=True, blank=True,
                              verify_exists=False)
    r_patrimony = models.ManyToManyField(EarthGeoDataPatrimony,
                                         verbose_name=_("patrimony recommendations"),
                                         null=True, blank=True)
    r_construction = models.ManyToManyField(EarthGeoDataConstruction,
                                           verbose_name=_("construction recommendations"),
                                           null=True, blank=True)
    r_meeting = models.ManyToManyField(EarthGeoDataMeeting,
                                       verbose_name=_("meeting recommendations"),
                                       null=True, blank=True)

