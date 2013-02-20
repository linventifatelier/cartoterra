from django.views.generic import DetailView
from django.views.generic.list import BaseListView
from models import Profile
from geodata.views import GeoJSONFeatureCollectionResponseMixin, GeoJSONListView
from geodata.models import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from sorl.thumbnail import get_thumbnail
from django.core.urlresolvers import reverse, reverse_lazy



class GeoJSONProfileCreatorMixin(GeoJSONFeatureCollectionResponseMixin):
    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileCreatorMixin, self).get_queryset(**kwargs)
        return queryset.filter(creator__username = self.kwargs['slug'])
         

class GeoJSONProfileCreatorListView(GeoJSONProfileCreatorMixin, BaseListView):
    pass
         

class GeoJSONProfileCreatorPatrimonyListView(GeoJSONProfileCreatorListView):
    model = EarthGeoDataPatrimony


class GeoJSONProfileCreatorConstructionListView(GeoJSONProfileCreatorListView):
    model = EarthGeoDataConstruction


class GeoJSONProfileCreatorMeetingListView(GeoJSONProfileCreatorListView):
    model = EarthGeoDataMeeting


class GeoJSONProfileCreatorActorListView(GeoJSONProfileCreatorListView):
    model = EarthGeoDataActor


class GeoJSONProfileRecommendListView(GeoJSONListView):
    def get_profile(self, **kwargs):
        return get_object_or_404(Profile, user__username=self.kwargs['slug'])


class GeoJSONProfileRecommendPatrimonyListView(GeoJSONProfileRecommendListView):
    model = EarthGeoDataPatrimony
    
    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendPatrimonyListView, self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in = profile.r_patrimony.all())


class GeoJSONProfileRecommendConstructionListView(GeoJSONProfileRecommendListView):
    model = EarthGeoDataConstruction

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendConstructionListView, self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in = profile.r_construction.all())


class GeoJSONProfileRecommendMeetingListView(GeoJSONProfileRecommendListView):
    model = EarthGeoDataMeeting
    
    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendMeetingListView, self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in = profile.r_meeting.all())


class GeoJSONProfileRecommendActorListView(GeoJSONProfileRecommendListView):
    model = EarthGeoDataActor
    
    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendActorListView, self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in = profile.r_actor.all())


class ProfileDetailView(DetailView):
    """Returns a template to present all patrimonies."""
    template_name = 'geodata/geodata_bigmap.html'
    module = "profilemap"
    model = Profile
    slug_field = 'user__username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)

        profile = get_object_or_404(Profile, user__username=self.kwargs['slug'])
        username = profile.user.username

        patrimonies = {
            'name': "Patrimonies %s" % username,
            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_creator_patrimony',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        constructions = {
            'name': "Constructions %s" % username,
            'external_graphic': settings.STATIC_URL+"img/construction.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_creator_construction',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        meetings = {
            'name': "Meetings %s" % username,
            'external_graphic': settings.STATIC_URL+"img/meeting.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_creator_meeting',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        actors = {
            'name': "Actors %s" % username,
            'external_graphic' : settings.STATIC_URL+"img/actor.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_creator_actor',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        recommendations_patrimonies = {
            'name': "Recommendations %s: Patrimonies" % username,
            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_recommend_patrimony',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        recommendations_constructions = {
            'name': "Recommendations %s: Constructions" % username,
            'external_graphic': settings.STATIC_URL+"img/construction.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_recommend_construction',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        recommendations_meetings = {
            'name': "Recommendations %s: Meetings" % username,
            'external_graphic': settings.STATIC_URL+"img/meeting.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_recommend_meeting',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        recommendations_actors = {
            'name': "Recommendations %s: Actors" % username,
            'external_graphic' : settings.STATIC_URL+"img/actor.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url' : reverse_lazy('geojson_profile_recommend_actor',
                                 kwargs={'slug' : self.kwargs['slug']}),
        }
        context['map_layers'] = [patrimonies, constructions, meetings, actors, recommendations_patrimonies, recommendations_constructions, recommendations_meetings, recommendations_actors]
        context['module'] = self.module
        return context

