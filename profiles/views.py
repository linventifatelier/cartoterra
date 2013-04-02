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


class GeoJSONProfileCreatorBuildingListView(GeoJSONProfileCreatorListView):
    model = models.Building


class GeoJSONProfileCreatorWorksiteListView(GeoJSONProfileCreatorListView):
    model = models.Worksite


class GeoJSONProfileCreatorEventListView(GeoJSONProfileCreatorListView):
    model = models.Event


class GeoJSONProfileCreatorStakeholderListView(GeoJSONProfileCreatorListView):
    model = models.Stakeholder


class GeoJSONProfileRecommendListView(GeoJSONListView):
    def get_profile(self, **kwargs):
        return get_object_or_404(Profile, user__username=self.kwargs['slug'])


class GeoJSONProfileRecommendBuildingListView(
        GeoJSONProfileRecommendListView):
    model = models.Building

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendBuildingListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_patrimony.all())


class GeoJSONProfileRecommendWorksiteListView(
        GeoJSONProfileRecommendListView):
    model = models.Worksite

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendWorksiteListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_construction.all())


class GeoJSONProfileRecommendEventListView(GeoJSONProfileRecommendListView):
    model = models.Event

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendEventListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_meeting.all())


class GeoJSONProfileRecommendStakeholderListView(
    GeoJSONProfileRecommendListView
):
    model = models.Stakeholder

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendStakeholderListView,
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
            'external_graphic': settings.STATIC_URL + "img/patrimony.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_patrimony',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        constructions = {
            'name': "Constructions %s" % username,
            'external_graphic': settings.STATIC_URL + "img/construction.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_construction',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        meetings = {
            'name': "Meetings %s" % username,
            'external_graphic': settings.STATIC_URL + "img/meeting.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_meeting',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        actors = {
            'name': "Actors %s" % username,
            'external_graphic': settings.STATIC_URL + "img/actor.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_actor',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_patrimonies = {
            'name': "Recommendations %s: Patrimonies" % username,
            'external_graphic': settings.STATIC_URL + "img/patrimony.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_patrimony',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_constructions = {
            'name': "Recommendations %s: Constructions" % username,
            'external_graphic': settings.STATIC_URL + "img/construction.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_construction',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_meetings = {
            'name': "Recommendations %s: Meetings" % username,
            'external_graphic': settings.STATIC_URL + "img/meeting.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_meeting',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_actors = {
            'name': "Recommendations %s: Actors" % username,
            'external_graphic': settings.STATIC_URL + "img/actor.png",
            'graphic_width': 10,
            'graphic_height': 10,
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
