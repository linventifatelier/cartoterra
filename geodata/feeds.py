#from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import Feed
from django.contrib.gis.feeds import GeoRSSFeed
from django.utils.translation import ugettext_lazy as _
#from django.contrib.gis.feeds import Feed
from django.conf import settings
from geodata.models import Building, Worksite, Event, Stakeholder, EarthGroup
import itertools


class BuildingFeed(Feed):
    """A feed presenting changes and additions on Building."""
    title = settings.SITE_NAME + " building news."
    link = "/"
    description = _("Updates on changes and additions to buildings of " +
                    settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return Building.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class WorksiteFeed(Feed):
    """A feed presenting changes and additions on Worksite."""
    title = _(settings.SITE_NAME + " worksite news.")
    link = "/"
    description = _("Updates on changes and additions to worksites of " +
                    settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return Worksite.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class EventFeed(Feed):
    """A feed presenting changes and additions on Event."""
    title = _(settings.SITE_NAME + " event news.")
    link = "/"
    description = _("Updates on changes and additions to events of " +
                    settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return Event.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class StakeholderFeed(Feed):
    """A feed presenting changes and additions on Stakeholder."""
    title = _(settings.SITE_NAME + " stakeholder news.")
    link = "/"
    description = _("Updates on changes and additions to stakeholders of " +
                    settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    #def item_extra_kwargs(self, item):
    #    return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        return Stakeholder.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class GeodataFeed(Feed):
    """A feed presenting changes and additions on cartoterra."""
    title = _(settings.SITE_NAME + " new entries.")
    link = "/"
    description = _("Updates on changes and additions to geodata of " +
                    settings.SITE_NAME + ".")

    feed_type = GeoRSSFeed

    def item_geometry(self, item):
        return item.geometry

    def items(self):
        queryset = list(itertools.chain(
            Building.objects.order_by('-pub_date')[:20],
            Worksite.objects.order_by('-pub_date')[:20],
            Event.objects.order_by('-pub_date')[:20],
            Stakeholder.objects.order_by('-pub_date')[:20]
        ))
        return sorted(queryset, key=lambda x:x.pub_date, reverse=True)[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description


class EarthGroupFeed(Feed):
    """A feed presenting changes and additions on EarthGroup."""
    title = _(settings.SITE_NAME + " group news.")
    link = "/"
    description = _("Updates on changes and additions to groups of " +
                    settings.SITE_NAME + ".")

    def items(self):
        return EarthGroup.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
