from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from models import Profile
import account.views
import geodata
from olwidget.widgets import InfoMap, Map, InfoLayer
from geodata.models import *
from django.shortcuts import get_object_or_404
from django.conf import settings


def _info_builder(geodataobjects, style = {}):
    info = []

    for i in geodataobjects:
        description = ""
        image = ""

        if i.description:
            description = i.description
        else: description = i.name

        if i.image:
            thumbnail = get_thumbnail(i.image, '100x100')
            image = "<p><a href=" + i.get_absolute_url() +\
                    "><img src=\"" + thumbnail.url + "\" width=\"" +\
                    str(thumbnail.x) + "\" height=\"" + str(thumbnail.y) +\
                    "\"></a></p>"

        mydict = { 'html': "<h1>" + i.name + "</h1>" +\
                       "<p><a href=" + i.get_absolute_url() + ">" +\
                       description + "</a></p>" + image,
                   'style': style
                   }

        info.append([ i.geometry, mydict ])
    return info



class ProfileDetail(DetailView):
    model = Profile
    template_name = 'show_usermap.html'
    slug_field = 'user__username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user__username=self.kwargs['slug'])
        user_ = profile.user
        patrimony = EarthGeoDataPatrimony.objects.filter(creator = user_)
        construction = EarthGeoDataConstruction.objects.filter(creator = user_)
        meeting = EarthGeoDataMeeting.objects.filter(creator = user_)
        actor = EarthGeoDataActor.objects.filter(creator = user_)
        r_patrimony = profile.r_patrimony.all()
        r_construction = profile.r_construction.all()
        r_meeting = profile.r_meeting.all()
        r_actor = profile.r_actor.all()
        lcount_patrimony = patrimony.count()
        lcount_construction = construction.count()
        lcount_meeting = meeting.count()
        lcount_actor = actor.count()
        lcount = lcount_patrimony + lcount_construction + lcount_meeting + lcount_actor
        lcount_r_patrimony = r_patrimony.count()
        lcount_r_construction = r_construction.count()
        lcount_r_meeting = r_meeting.count()
        lcount_r_actor = r_actor.count()
        lcount_r = lcount_r_patrimony + lcount_r_construction + lcount_r_meeting + lcount_r_actor
        name = user_.username

        map_ = Map([
           InfoLayer(_info_builder(patrimony),
                     {'name': "Patrimonies " + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(construction),
                     {'name': "Constructions " + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/construction.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(meeting),
                     {'name': "Meetings " + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/meeting.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(actor),
                     {'name': "Actors" + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/actor.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(r_patrimony),
                     {'name': "Recommendations: Patrimonies " + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                          'graphic_width': 10,
                          'graphic_height': 10,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(r_construction),
                     {'name': "Recommendations: Constructions " + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/construction.png",
                          'graphic_width': 10,
                          'graphic_height': 10,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(r_meeting),
                     {'name': "Recommendations: Meetings " + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/meeting.png",
                          'graphic_width': 10,
                          'graphic_height': 10,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(r_actor),
                     {'name': "Recommendations: Actors " + name,
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/actor.png",
                          'graphic_width': 10,
                          'graphic_height': 10,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
        ], {'map_div_class': 'usermap'})
        context['user_'] = user_
        context['location_count'] = lcount
        context['patrimony_count'] = lcount_patrimony
        context['construction_count'] = lcount_construction
        context['meeting_count'] = lcount_meeting
        context['actor_count'] = lcount_actor
        context['r_location_count'] = lcount_r
        context['r_patrimony_count'] = lcount_r_patrimony
        context['r_construction_count'] = lcount_r_construction
        context['r_meeting_count'] = lcount_r_meeting
        context['r_actor_count'] = lcount_r_actor
        context['map'] = map_
        return context



def show_usermap(request, userid):
    """Returns a show_usermap.html template."""
    profile = get_object_or_404(Profile, pk=userid)
    user_ = profile.user
    patrimony = EarthGeoDataPatrimony.objects.filter(creator = user_)
    construction = EarthGeoDataConstruction.objects.filter(creator = user_)
    meeting = EarthGeoDataMeeting.objects.filter(creator = user_)
    actor = EarthGeoDataActor.objects.filter(creator = user_)
    r_patrimony = profile.r_patrimony.all()
    r_construction = profile.r_construction.all()
    r_meeting = profile.r_meeting.all()
    r_actor = profile.r_actor.all()
    lcount_patrimony = patrimony.count()
    lcount_construction = construction.count()
    lcount_meeting = meeting.count()
    lcount_actor = actor.count()
    lcount = lcount_patrimony + lcount_construction + lcount_meeting + lcount_actor
    lcount_r_patrimony = r_patrimony.count()
    lcount_r_construction = r_construction.count()
    lcount_r_meeting = r_meeting.count()
    lcount_r_actor = r_actor.count()
    lcount_r = lcount_r_patrimony + lcount_r_construction + lcount_r_meeting + lcount_r_actor
    name = user_.username

    map_ = Map([
       InfoLayer(_info_builder(patrimony),
                 {'name': "Patrimonies " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(construction),
                 {'name': "Constructions " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/construction.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(meeting),
                 {'name': "Meetings " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/meeting.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(actor),
                 {'name': "Actors" + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/actor.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_patrimony),
                 {'name': "Recommendations: Patrimonies " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                      'graphic_width': 10,
                      'graphic_height': 10,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_construction),
                 {'name': "Recommendations: Constructions " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/construction.png",
                      'graphic_width': 10,
                      'graphic_height': 10,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_meeting),
                 {'name': "Recommendations: Meetings " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/meeting.png",
                      'graphic_width': 10,
                      'graphic_height': 10,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_actor),
                 {'name': "Recommendations: Actors " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/actor.png",
                      'graphic_width': 10,
                      'graphic_height': 10,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
    ], {'map_div_class': 'usermap'})
    return direct_to_template(request, 'show_usermap.html',
                              { 'map': map_,
                                'user_': user_,
                                'location_count': lcount,
                                'patrimony_count': lcount_patrimony,
                                'construction_count': lcount_construction,
                                'meeting_count': lcount_meeting,
                                'actor_count': lcount_actor,
                                'r_location_count': lcount_r,
                                'r_patrimony_count': lcount_r_patrimony,
                                'r_construction_count': lcount_r_construction,
                                'r_meeting_count': lcount_r_meeting,
                                'r_actor_count': lcount_r_actor,
                                })
