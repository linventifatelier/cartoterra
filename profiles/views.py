from django.views.generic import DetailView, ListView
from django.views.generic.list import BaseListView
from models import Profile
from geodata.views import GeoJSONFeatureCollectionResponseMixin,\
    GeoJSONListView
from geodata import models
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse_lazy


class GeoJSONProfileCreatorMixin(GeoJSONFeatureCollectionResponseMixin):
    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileCreatorMixin,
                         self).get_queryset(**kwargs)
        return queryset.filter(creator__username=self.kwargs['slug'])


class GeoJSONProfileCreatorListView(GeoJSONProfileCreatorMixin, BaseListView):
    pass


class GeoJSONProfileCreatorPatrimonyListView(GeoJSONProfileCreatorListView):
    model = models.EarthGeoDataPatrimony


class GeoJSONProfileCreatorConstructionListView(GeoJSONProfileCreatorListView):
    model = models.EarthGeoDataConstruction


class GeoJSONProfileCreatorMeetingListView(GeoJSONProfileCreatorListView):
    model = models.EarthGeoDataMeeting


class GeoJSONProfileCreatorActorListView(GeoJSONProfileCreatorListView):
    model = models.EarthGeoDataActor


class GeoJSONProfileRecommendListView(GeoJSONListView):
    def get_profile(self, **kwargs):
        return get_object_or_404(Profile, user__username=self.kwargs['slug'])


class GeoJSONProfileRecommendPatrimonyListView(
        GeoJSONProfileRecommendListView):
    model = models.EarthGeoDataPatrimony

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendPatrimonyListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_patrimony.all())


class GeoJSONProfileRecommendConstructionListView(
        GeoJSONProfileRecommendListView):
    model = models.EarthGeoDataConstruction

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendConstructionListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_construction.all())


class GeoJSONProfileRecommendMeetingListView(GeoJSONProfileRecommendListView):
    model = models.EarthGeoDataMeeting

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendMeetingListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_meeting.all())


class GeoJSONProfileRecommendActorListView(GeoJSONProfileRecommendListView):
    model = models.EarthGeoDataActor

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendActorListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_actor.all())


class ProfileDetailView(DetailView):
    """Returns a template to present all patrimonies of a given profile."""
    template_name = 'profilemap.html'
    module = "profilemap"
    model = Profile
    slug_field = 'user__username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)

        profile = get_object_or_404(Profile,
                                    user__username=self.kwargs['slug'])
        username = profile.user.username

        patrimonies = {
            'name': "Patrimonies %s" % username,
            'external_graphic': settings.STATIC_URL + "img/buildings_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_patrimony',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        constructions = {
            'name': "Constructions %s" % username,
            'external_graphic': settings.STATIC_URL + "img/construction_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_construction',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        meetings = {
            'name': "Meetings %s" % username,
            'external_graphic': settings.STATIC_URL + "img/event_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_meeting',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        actors = {
            'name': "Actors %s" % username,
            'external_graphic': settings.STATIC_URL + "img/stakeholder_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_actor',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_patrimonies = {
            'name': "Recommendations %s: Patrimonies" % username,
            'external_graphic': settings.STATIC_URL + "img/building_icon_h25.png",
            'graphic_width': 15,
            'graphic_height': 15,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_patrimony',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_constructions = {
            'name': "Recommendations %s: Constructions" % username,
            'external_graphic': settings.STATIC_URL + "img/construction_icon_h25.png",
            'graphic_width': 15,
            'graphic_height': 15,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_construction',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_meetings = {
            'name': "Recommendations %s: Meetings" % username,
            'external_graphic': settings.STATIC_URL + "img/event_icon_h25.png",
            'graphic_width': 15,
            'graphic_height': 15,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_meeting',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_actors = {
            'name': "Recommendations %s: Actors" % username,
            'external_graphic': settings.STATIC_URL + "img/stakeholder_icon_h25.png",
            'graphic_width': 15,
            'graphic_height': 15,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_actor',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        context['map_layers'] = [patrimonies, constructions, meetings, actors,
                                 recommendations_patrimonies,
                                 recommendations_constructions,
                                 recommendations_meetings,
                                 recommendations_actors]
        context['module'] = self.module
        return context


class ProfileListView(ListView):
    """Returns a template to present all profiles."""
    model = Profile
    template_name = 'profile_list.html'
