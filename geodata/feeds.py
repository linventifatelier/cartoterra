#from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import Feed
from django.contrib.gis.feeds import GeoRSSFeed
from django.utils.translation import ugettext_lazy as _
#from django.contrib.gis.feeds import Feed
from django.conf import settings
from geodata.models import EarthGeoDataPatrimony, EarthGeoDataConstruction,\
    EarthGeoDataMeeting


class PatrimonyFeed(Feed):
    """A feed presenting changes and additions on EarthGeoDataPatrimony."""
    title = settings.SITE_NAME + " patrimony news."
    link = "/"
    description = _("Updates on changes and additions to patrimonies of " + settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return EarthGeoDataPatrimony.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class ConstructionFeed(Feed):
    """A feed presenting changes and additions on EarthGeoDataConstruction."""
    title = _(settings.SITE_NAME + " construction news.")
    link = "/"
    description = _("Updates on changes and additions to constructions of " + settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return EarthGeoDataConstruction.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class MeetingFeed(Feed):
    """A feed presenting changes and additions on EarthGeoDataMeeting."""
    title = _(settings.SITE_NAME + " meeting news.")
    link = "/"
    description = _("Updates on changes and additions to meetings of " + settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return EarthGeoDataMeeting.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class ActorFeed(Feed):
    """A feed presenting changes and additions on EarthGeoDataActor."""
    title = _(settings.SITE_NAME + " actor news.")
    link = "/"
    description = _("Updates on changes and additions to actors of " + settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return EarthGeoDataMeeting.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
