from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from geodata.models import Building, Worksite, Event, Stakeholder
from django.db.models.signals import post_save


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
        Building,
        verbose_name=_("building recommendations"),
        null=True, blank=True)
    r_construction = models.ManyToManyField(
        Worksite,
        verbose_name=_("worksite recommendations"),
        null=True, blank=True)
    r_meeting = models.ManyToManyField(
        Event,
        verbose_name=_("event recommendations"),
        null=True, blank=True)
    r_actor = models.ManyToManyField(
        Stakeholder,
        verbose_name=_("stakeholder recommendations"),
        null=True, blank=True)

    def recommends(self, geodata):
        if isinstance(geodata, Building):
            return self.r_patrimony.filter(id=geodata.id).exists()
        elif isinstance(geodata, Worksite):
            return self.r_construction.filter(id=geodata.id).exists()
        elif isinstance(geodata, Event):
            return self.r_meeting.filter(id=geodata.id).exists()
        elif isinstance(geodata, Stakeholder):
            return self.r_actor.filter(id=geodata.id).exists()
        else:
            return False


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
