#from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import Feed
from django.contrib.gis.feeds import GeoRSSFeed
from django.utils.translation import ugettext_lazy as _
#from django.contrib.gis.feeds import Feed
from django.conf import settings
from geodata.models import Building, Worksite, Event, Stakeholder


class BuildingFeed(Feed):
    """A feed presenting changes and additions on Building."""
    title = settings.SITE_NAME + " patrimony news."
    link = "/"
    description = _("Updates on changes and additions to patrimonies of " +
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
    title = _(settings.SITE_NAME + " construction news.")
    link = "/"
    description = _("Updates on changes and additions to constructions of " +
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
    title = _(settings.SITE_NAME + " meeting news.")
    link = "/"
    description = _("Updates on changes and additions to meetings of " +
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
    title = _(settings.SITE_NAME + " actor news.")
    link = "/"
    description = _("Updates on changes and additions to actors of " +
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
