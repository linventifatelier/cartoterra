from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from geodata.models import EarthGeoDataPatrimony, EarthGeoDataConstruction, \
    EarthGeoDataMeeting, EarthGeoDataActor
from django.db.models.signals import post_save
from account.models import *


class Profile(models.Model):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'))
    #about = models.TextField(_("about"), null=True, blank=True)
    #location = models.CharField(_("location"), max_length=40, null=True,
    #                            blank=True)
    #website = models.URLField(_("website"), null=True, blank=True,
    #                          verify_exists=False)
    r_patrimony = models.ManyToManyField(
        EarthGeoDataPatrimony,
        verbose_name=_("patrimony recommendations"),
        null=True, blank=True)
    r_construction = models.ManyToManyField(
        EarthGeoDataConstruction,
        verbose_name=_("construction recommendations"),
        null=True, blank=True)
    r_meeting = models.ManyToManyField(
        EarthGeoDataMeeting,
        verbose_name=_("meeting recommendations"),
        null=True, blank=True)
    r_actor = models.ManyToManyField(
        EarthGeoDataActor,
        verbose_name=_("actor recommendations"),
        null=True, blank=True)

    def recommends(self, geodata):
        if isinstance(geodata, EarthGeoDataPatrimony):
            return self.r_patrimony.filter(id=geodata.id).exists()
        elif isinstance(geodata, EarthGeoDataConstruction):
            return self.r_construction.filter(id=geodata.id).exists()
        elif isinstance(geodata, EarthGeoDataMeeting):
            return self.r_meeting.filter(id=geodata.id).exists()
        elif isinstance(geodata, EarthGeoDataActor):
            return self.r_actor.filter(id=geodata.id).exists()
        else:
            return False


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
