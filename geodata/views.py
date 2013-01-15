"""GeoData views."""

from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from models import EarthGeoDataPatrimony, EarthGeoDataConstruction,\
     EarthGeoDataMeeting, EarthGeoDataActor
from forms import EarthGeoDataPatrimonyForm, EarthGeoDataConstructionForm,\
     EarthGeoDataMeetingForm, EarthGeoDataActorForm
from olwidget.widgets import InfoMap, Map, InfoLayer
from sorl.thumbnail import get_thumbnail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User
from profiles.models import Profile
from django.conf import settings
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.utils import simplejson
from django.views.generic.detail import BaseDetailView, \
    SingleObjectTemplateResponseMixin
from django.utils.decorators import method_decorator








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


class PatrimonyListView(ListView):
    """Returns a template to present all patrimonies."""
    model = EarthGeoDataPatrimony
    context_object_name = 'geodata'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatrimonyListView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataPatrimony.objects.all()
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Patrimonies",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class PatrimonyContemporaryView(PatrimonyListView):
    """Returns a template to present contemporary patrimonies."""
    template_name = 'show_patrimony_all.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatrimonyContemporaryView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataPatrimony.objects.filter(
            inauguration_date__gte = datetime.now() - timedelta(days=3650))
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Patrimonies",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class PatrimonyUnescoView(PatrimonyListView):
    """Returns a template to present unesco patrimonies."""
    template_name = 'show_patrimony_all.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatrimonyUnescoView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataPatrimony.objects.filter(unesco = True)
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Patrimonies",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class PatrimonyVernacularView(PatrimonyListView):
    """Returns a template to present vernacular patrimonies."""
    template_name = 'show_patrimony_all.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatrimonyVernacularView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataPatrimony.objects.filter(architects__isnull = True)
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Patrimonies",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class PatrimonyNormalView(PatrimonyListView):
    """Returns a template to present normal patrimonies."""
    template_name = 'show_patrimony_all.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatrimonyNormalView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataPatrimony.objects.filter(
            Q(architects__isnull = False) & Q(unesco = False) &
            (Q(inauguration_date__isnull = True) |
             ~Q(inauguration_date__gte = datetime.now() - timedelta(days=3650))))
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Patrimonies",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class ConstructionListView(ListView):
    """Returns a template to present all constructions."""
    model = EarthGeoDataConstruction
    context_object_name = 'geodata'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ConstructionListView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataConstruction.objects.all()
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Constructions",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/construction.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class ConstructionParticipativeView(ConstructionListView):
    """Returns a template to present participative constructions."""

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ConstructionParticipativeView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataConstruction.objects.filter(participative = True)
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Constructions",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/construction.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class ConstructionNormalView(ConstructionListView):
    """Returns a template to present normal constructions."""
    template_name = 'show_construction_all.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ConstructionNormalView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataConstruction.objects.filter(participative = False)
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Constructions",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/construction.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class MeetingListView(ListView):
    """Returns a template to present all meetings."""
    model = EarthGeoDataMeeting
    context_object_name = 'geodata'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MeetingListView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataMeeting.objects.all()
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Meetings",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/meeting.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class MeetingSeminarView(MeetingListView):
    """Returns a template to present seminar meetings."""

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MeetingSeminarView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataMeeting.objects.filter(meeting_type='S')
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Meetings",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/meeting.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class MeetingColloquiumView(MeetingListView):
    """Returns a template to present colloquium meetings."""

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MeetingColloquiumView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataMeeting.objects.filter(meeting_type='Q')
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Meetings",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/meeting.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class MeetingConferenceView(MeetingListView):
    """Returns a template to present conference meetings."""

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MeetingConferenceView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataMeeting.objects.filter(meeting_type='C')
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Meetings",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/meeting.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class MeetingFestivalView(TemplateView):
    """Returns a template to present festival meetings."""
    template_name = 'show_meeting_all.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MeetingFestivalView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataMeeting.objects.filter(meeting_type='F')
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Meetings",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/meeting.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class ActorListView(ListView):
    """Returns a template to present all meetings."""
    model = EarthGeoDataActor
    context_object_name = 'geodata'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ActorListView, self).get_context_data(**kwargs)

        geodata_list = EarthGeoDataActor.objects.all()
        map_ = InfoMap(_info_builder(geodata_list),
                       {'name': "Actors",
                        'overlay_style': {
                            'external_graphic': settings.STATIC_URL+"img/actor.png",
                            'graphic_width': 20,
                            'graphic_height': 20,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            },
                        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                        })

        context['geodata_list'] = geodata_list
        context['map'] = map_
        return context


class BigMapView(TemplateView):
    """Returns a big Map with all geodatas."""
    __name__ = 'show_bigmap'

    template_name = 'show_bigmap.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BigMapView, self).get_context_data(**kwargs)

        patrimony = EarthGeoDataPatrimony.objects.all()
        construction = EarthGeoDataConstruction.objects.all()
        meeting = EarthGeoDataMeeting.objects.all()
        actor = EarthGeoDataActor.objects.all()
        lcount_patrimony = patrimony.count()
        lcount_construction = construction.count()
        lcount_meeting = meeting.count()
        lcount_actor = actor.count()
        lcount = lcount_patrimony + lcount_construction + lcount_meeting + lcount_actor

        map_ = Map([
           InfoLayer(_info_builder(patrimony),
                     {'name': "Patrimonies",
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(construction),
                     {'name': "Constructions",
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/construction.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(meeting),
                     {'name': "Meetings",
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/meeting.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
           InfoLayer(_info_builder(actor),
                     {'name': "Actors",
                      'overlay_style': {
                          'external_graphic': settings.STATIC_URL+"img/actor.png",
                          'graphic_width': 20,
                          'graphic_height': 20,
                          'fill_color': '#00FF00',
                          'stroke_color': '#008800',
                          }}),
        ], {'map_div_class': 'bigmap', 'map_div_style': {'width': '600px', 'height': '400px'}})

        context['map'] = map_
        context['location_count'] = lcount
        context['patrimony_count'] = lcount_patrimony
        context['construction_count'] = lcount_construction
        context['meeting_count'] = lcount_meeting
        context['actor_count'] = lcount_actor
        return context


def get_profilemap(profile):
    user_ = profile.user
    patrimony = EarthGeoDataPatrimony.objects.filter(creator = user_)
    construction = EarthGeoDataConstruction.objects.filter(creator = user_)
    meeting = EarthGeoDataMeeting.objects.filter(creator = user_)
    actor = EarthGeoDataActor.objects.filter(creator = user_)
    r_patrimony = profile.r_patrimony.all()
    r_construction = profile.r_construction.all()
    r_meeting = profile.r_meeting.all()
    r_actor = profile.r_actor.all()
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
       InfoLayer(_info_builder(r_patrimony, {
                            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                            'graphic_width': 10,
                            'graphic_height': 10,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            }) +
                 _info_builder(r_construction, {
                            'external_graphic': settings.STATIC_URL+"img/construction.png",
                            'graphic_width': 10,
                            'graphic_height': 10,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            }) +
                 _info_builder(r_meeting, {
                            'external_graphic': settings.STATIC_URL+"img/meeting.png",
                            'graphic_width': 10,
                            'graphic_height': 10,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            }) ,
                 _info_builder(r_actor, {
                            'external_graphic': settings.STATIC_URL+"img/actor.png",
                            'graphic_width': 10,
                            'graphic_height': 10,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            }) ,
                 {'name': "Recommendations " + name, }),
    ], {'map_div_class': 'usermap'})
    return map_


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


def _get_dict_show(request, map_, geodata, edit_func, delete_func,
                   toggle_rec_func, pk):
    user = request.user
    if isinstance(user, AnonymousUser):
        return {'map': map_, 'geodata': geodata, }
    else:
        if geodata.creator != request.user:
            profile = request.user.get_profile()
            recommendations = []
            if toggle_rec_func == 'toggle_rec_patrimony':
                recommendations = profile.r_patrimony
            elif toggle_rec_func == 'toggle_rec_construction':
                recommendations = profile.r_construction
            elif toggle_rec_func == 'toggle_rec_meeting':
                recommendations = profile.r_meeting
            elif toggle_rec_func == 'toggle_rec_actor':
                recommendations = profile.r_actor
                if geodata in recommendations.all():
                    return {'map': map_, 'geodata': geodata,
                            'rec_off_geodata': reverse(toggle_rec_func, args=[pk]), }
                else:
                    return {'map': map_, 'geodata': geodata,
                            'rec_on_geodata': reverse(toggle_rec_func, args=[pk]), }
        else:
            return {'map': map_, 'geodata': geodata,
                    'edit_geodata': reverse(edit_func, args=[pk]),
                    'delete_geodata': reverse(delete_func, args=[pk]),}


class PatrimonyDetail(DetailView):
    model = EarthGeoDataPatrimony
    context_object_name = 'geodata'
    
    def get_context_data(self, **kwargs):
        context = super(PatrimonyDetail, self).get_context_data(**kwargs)

        geodata = get_object_or_404(EarthGeoDataPatrimony, pk=self.kwargs['pk'])
        map_ = InfoMap([[geodata.geometry,
                         { 'style': {
                             'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                             'graphic_width': 30,
                             'graphic_height': 30,
                             'fill_color': '#00FF00',
                             'stroke_color': '#008800',
                             }}]],
                       { 'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }}
                       )
        dict_show = _get_dict_show(self.request, map_, geodata, 'edit_patrimony', 'delete_patrimony', 'toggle_rec_patrimony', pk=self.kwargs['pk'])
        context.update(dict_show)
        return context
    

class ConstructionDetail(DetailView):
    model = EarthGeoDataConstruction
    context_object_name = 'geodata'
    
    def get_context_data(self, **kwargs):
        context = super(ConstructionDetail, self).get_context_data(**kwargs)

        geodata = get_object_or_404(EarthGeoDataConstruction, pk=self.kwargs['pk'])
        map_ = InfoMap([[geodata.geometry,
                         { 'style': {
                             'external_graphic': settings.STATIC_URL+"img/construction.png",
                             'graphic_width': 30,
                             'graphic_height': 30,
                             'fill_color': '#00FF00',
                             'stroke_color': '#008800',
                             }}]],
                       { 'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }}
                       )
        dict_show = _get_dict_show(self.request, map_, geodata, 'edit_construction', 'delete_construction', 'toggle_rec_construction', pk=self.kwargs['pk'])
        context.update(dict_show)
        return context



class MeetingDetail(DetailView):
    model = EarthGeoDataMeeting
    context_object_name = 'geodata'
    
    def get_context_data(self, **kwargs):
        context = super(MeetingDetail, self).get_context_data(**kwargs)

        geodata = get_object_or_404(EarthGeoDataMeeting, pk=self.kwargs['pk'])
        map_ = InfoMap([[geodata.geometry,
                         { 'style': {
                             'external_graphic': settings.STATIC_URL+"img/meeting.png",
                             'graphic_width': 30,
                             'graphic_height': 30,
                             'fill_color': '#00FF00',
                             'stroke_color': '#008800',
                             }}]],
                       { 'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }}
                       )
        dict_show = _get_dict_show(self.request, map_, geodata, 'edit_meeting', 'delete_meeting', 'toggle_rec_meeting', pk=self.kwargs['pk'])
        context.update(dict_show)
        return context


class ActorDetail(DetailView):
    model = EarthGeoDataActor
    context_object_name = 'geodata'
    
    def get_context_data(self, **kwargs):
        context = super(ActorDetail, self).get_context_data(**kwargs)

        geodata = get_object_or_404(EarthGeoDataActor, pk=self.kwargs['pk'])
        map_ = InfoMap([[geodata.geometry,
                         { 'style': {
                             'external_graphic': settings.STATIC_URL+"img/actor.png",
                             'graphic_width': 30,
                             'graphic_height': 30,
                             'fill_color': '#00FF00',
                             'stroke_color': '#008800',
                             }}]],
                       { 'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }}
                       )
        dict_show = _get_dict_show(self.request, map_, geodata, 'edit_actor', 'delete_actor', 'toggle_rec_actor', pk=self.kwargs['pk'])
        context.update(dict_show)
        return context



error_message = _("Please correct the errors below.")


@login_required
def _add_builder(request, geodatamodel, geodatamodelform, geodatatemplate):
    geodata = geodatamodel(creator = request.user,
                           pub_date = datetime.now())

    if request.method == "POST":
        form = geodatamodelform(request.POST, request.FILES, instance = geodata)
        if form.is_valid():
            obj = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully added %(modelname)s \"%(name)s\".") %
                                 {'modelname': force_unicode(obj._meta.verbose_name), 'name': obj.name,}
                                 )
            return HttpResponseRedirect('%s' % obj.get_absolute_url())
        else:
            messages.add_message(request, messages.ERROR,
                                 error_message
                                 )
    else:
        form = geodatamodelform(instance = geodata) # An unbound form

    return direct_to_template(request, geodatatemplate, {
            'form': form,
            })



class PatrimonyCreateView(CreateView):
    model = EarthGeoDataPatrimony
    form_class = EarthGeoDataPatrimonyForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PatrimonyCreateView, self).dispatch(*args, **kwargs)


@login_required
def add_patrimony(request):
    return _add_builder(request, EarthGeoDataPatrimony, EarthGeoDataPatrimonyForm, 'add_patrimony.html')


@login_required
def add_construction(request):
    return _add_builder(request, EarthGeoDataConstruction, EarthGeoDataConstructionForm, 'add_construction.html')


@login_required
def add_meeting(request):
    return _add_builder(request, EarthGeoDataMeeting, EarthGeoDataMeetingForm, 'add_meeting.html')


@login_required
def add_actor(request):
    return _add_builder(request, EarthGeoDataActor, EarthGeoDataActorForm, 'add_actor.html')



@login_required
def _edit_builder(request, geodatamodel, geodatamodelform, geodatatemplate, ident):
    geodata = get_object_or_404(geodatamodel, pk=ident)
    if geodata.creator != request.user:
        messages.add_message(request, messages.ERROR,
                             _("You cannot edit %(modelname)s \"%(name)s\"") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
        return HttpResponseForbidden()

    if request.method == "POST":
        form = geodatamodelform(request.POST, request.FILES, instance = geodata)
        if form.is_valid():
            obj = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully edited %(modelname)s \"%(name)s\".") %
                                 { 'modelname': force_unicode(obj._meta.verbose_name), 'name': obj.name, }
                                 )
            return HttpResponseRedirect("%s" % obj.get_absolute_url())
            #return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.ERROR,
                                 error_message
                                 )
    else:
        form = geodatamodelform(instance = geodata) # An unbound form

    return direct_to_template(request, geodatatemplate, {
        'form': form,
        'geodata': geodata,
        })


@login_required
def edit_patrimony(request, ident):
    return _edit_builder(request, EarthGeoDataPatrimony,
                         EarthGeoDataPatrimonyForm, 'edit_patrimony.html', ident)



@login_required
def edit_construction(request, ident):
    return _edit_builder(request, EarthGeoDataConstruction,
                         EarthGeoDataConstructionForm, 'edit_construction.html', ident)


@login_required
def edit_meeting(request, ident):
    return _edit_builder(request, EarthGeoDataMeeting,
                         EarthGeoDataMeetingForm, 'edit_meeting.html', ident)


@login_required
def edit_actor(request, ident):
    return _edit_builder(request, EarthGeoDataActor,
                         EarthGeoDataActorForm, 'edit_actor.html', ident)


@login_required
def _delete_builder(request, geodatamodel, geodatatemplate, ident):
    geodata = get_object_or_404(geodatamodel, pk=ident)

    if geodata.creator != request.user:
        messages.add_message(request, messages.ERROR,
                             _("You cannot delete %(modelname)s \"%(name)s\"") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
        return HttpResponseForbidden()

    if request.method == 'POST':
        geodata.delete()
        messages.add_message(request, messages.SUCCESS,
                             _("Successfully deleted %(modelname)s \"%(name)s\".") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
        return HttpResponseRedirect('/')
    else:
        return direct_to_template(request, geodatatemplate, {
            'geodata': geodata,
        })


@login_required
def delete_patrimony(request, ident):
    return _delete_builder(request, EarthGeoDataPatrimony, 'delete_patrimony.html', ident)


@login_required
def delete_construction(request, ident):
    return _delete_builder(request, EarthGeoDataConstruction, 'delete_construction.html', ident)


@login_required
def delete_meeting(request, ident):
    return _delete_builder(request, EarthGeoDataMeeting, 'delete_meeting.html', ident)


@login_required
def delete_actor(request, ident):
    return _delete_builder(request, EarthGeoDataActor, 'delete_actor.html', ident)


@login_required
def _toggle_recommendation(request, geodatamodel, profile_r, ident):
    geodata = get_object_or_404(geodatamodel, pk=ident)
    profile = request.user.get_profile()

    if request.user == geodata.creator:
        messages.add_message(request, messages.ERROR,
                             _("You cannot recommend %(modelname)s \"%(name)s\".") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
    else:
        if geodata in profile_r.all():
            profile_r.remove(geodata)
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully removed %(modelname)s \"%(name)s\" \
                             from your recommendations.") %
                                 { 'modelname': force_unicode(geodata._meta.verbose_name),
                                   'name': geodata.name, }
                                 )
        else:
            profile_r.add(geodata)
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully added %(modelname)s \"%(name)s\" \
                             to your recommendations.") %
                                 { 'modelname': force_unicode(geodata._meta.verbose_name),
                                   'name': geodata.name, }
                                 )
    return HttpResponseRedirect('%s' % geodata.get_absolute_url())

@login_required
def toggle_rec_patrimony(request, ident):
    profile = request.user.get_profile()
    return _toggle_recommendation(request = request,
                                  geodatamodel = EarthGeoDataPatrimony,
                                  profile_r = profile.r_patrimony,
                                  ident = ident)


@login_required
def toggle_rec_construction(request, ident):
    profile = request.user.get_profile()
    return _toggle_recommendation(request = request,
                                  geodatamodel = EarthGeoDataConstruction,
                                  profile_r = profile.r_construction,
                                  ident = ident)


@login_required
def toggle_rec_meeting(request, ident):
    profile = request.user.get_profile()
    return _toggle_recommendation(request = request,
                                  geodatamodel = EarthGeoDataMeeting,
                                  profile_r = profile.r_meeting,
                                  ident = ident)


@login_required
def toggle_rec_actor(request, ident):
    profile = request.user.get_profile()
    return _toggle_recommendation(request = request,
                                  geodatamodel = EarthGeoDataActor,
                                  profile_r = profile.r_actor,
                                  ident = ident)


class TestView(TemplateView):
    template_name = 'test.html'
