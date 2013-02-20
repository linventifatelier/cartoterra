"""GeoData views."""

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from models import EarthGeoDataPatrimony, EarthGeoDataConstruction,\
     EarthGeoDataMeeting, EarthGeoDataActor, EarthGeoDataAbstract
from forms import EarthGeoDataPatrimonyForm, EarthGeoDataConstructionForm,\
     EarthGeoDataMeetingForm, EarthGeoDataActorForm
from olwidget.widgets import InfoMap, Map, InfoLayer
from sorl.thumbnail import get_thumbnail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from profiles.models import Profile
from django.conf import settings
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import SingleObjectMixin, DetailView, BaseDetailView
from django.views.generic.list import ListView, BaseListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize



class GeoJSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a GeoJSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)


class GeoJSONFeatureResponseMixin(GeoJSONResponseMixin):
    def convert_context_to_json(self, context):
        "Convert the context dictionary into a GeoJSON object"
        m = self.get_object()
        data = {'crs': {"type": "link", "properties": {"href": "http://spatialreference.org/ref/epsg/4326/", "type": "proj4"}},
                'type': "Feature",
                'geometry': simplejson.loads(m.geometry.geojson),
                'properties': { 'pk': m.pk, 'name': m.name,
                                'url': m.get_absolute_url(),
                                'image': get_thumbnail(m.image, '100x100').url if m.image else None, }}
        return simplejson.dumps(data)
            

class GeoJSONFeatureCollectionResponseMixin(GeoJSONResponseMixin):
    def convert_context_to_json(self, context):
        "Convert the context dictionary into a GeoJSON object"
        queryset = self.get_queryset()
        data = {"crs": {"type": "link", "properties": {"href": "http://spatialreference.org/ref/epsg/4326/", "type": "proj4"}},
                "type": "FeatureCollection",
                "features": [{ 'geometry': simplejson.loads(m.geometry.geojson),
                               'type': "Feature",
                               'properties': { 'pk': m.pk, 'name': m.name,
                                               'url': m.get_absolute_url(),
                                               'image': get_thumbnail(m.image, '100x100').url if m.image else None,
                                             }} for m in queryset]}
        return simplejson.dumps(data)
            


class GeoJSONDetailView(GeoJSONFeatureResponseMixin, BaseDetailView):
    pass


class GeoJSONListView(GeoJSONFeatureCollectionResponseMixin, BaseListView):
    pass


class GeoJSONPatrimonyListView(GeoJSONListView):
    model = EarthGeoDataPatrimony


class GeoJSONPatrimonyDetailView(GeoJSONDetailView):
    model = EarthGeoDataPatrimony


class GeoJSONConstructionListView(GeoJSONListView):
    model = EarthGeoDataConstruction


class GeoJSONConstructionDetailView(GeoJSONDetailView):
    model = EarthGeoDataConstruction


class GeoJSONMeetingListView(GeoJSONListView):
    model = EarthGeoDataMeeting


class GeoJSONMeetingDetailView(GeoJSONDetailView):
    model = EarthGeoDataMeeting


class GeoJSONActorListView(GeoJSONListView):
    model = EarthGeoDataActor


class GeoJSONActorDetailView(GeoJSONDetailView):
    model = EarthGeoDataActor


class GeoDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GeoDataMixin, self).get_context_data(**kwargs)
        context['module'] = self.module
        context['map_layers'] = self.map_layers
        return context


class GeoDataListView(GeoDataMixin, ListView):
    pass


class PatrimonyListView(GeoDataListView):
    """Returns a template to present all patrimonies."""
    model = EarthGeoDataPatrimony
    context_object_name = 'geodata'
    module = "list"
    patrimonies = {
        'name': "Patrimonies",
        'external_graphic' : settings.STATIC_URL+"img/patrimony.png",
        'graphic_width' : 20,
        'graphic_height' : 20,
        'fill_color' : '#00FF00',
        'stroke_color' : '#008800',
        'url' : 'geojson/',
    }
    map_layers = [patrimonies]


class ConstructionListView(GeoDataListView):
    """Returns a template to present all constructions."""
    model = EarthGeoDataConstruction
    context_object_name = 'geodata'
    module = "list"
    constructions = {
        'name': "Constructions",
        'external_graphic': settings.STATIC_URL+"img/construction.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url' : 'geojson/',
    }
    map_layers = [constructions]


class MeetingListView(GeoDataListView):
    """Returns a template to present all meetings."""
    model = EarthGeoDataMeeting
    context_object_name = 'geodata'
    module = "list"
    meetings = {
        'name': "Meetings",
        'external_graphic': settings.STATIC_URL+"img/meeting.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url' : 'geojson/',
    }
    map_layers = [meetings]


class ActorListView(GeoDataListView):
    """Returns a template to present all actors."""
    model = EarthGeoDataActor
    context_object_name = 'geodata'
    module = "list"
    actors = {
        'name': "Actors",
        'external_graphic': settings.STATIC_URL+"img/actor.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url' : 'geojson/',
    }
    map_layers = [actors]


class GeoDataTemplateView(GeoDataMixin, TemplateView):
    pass


class BigMapView(GeoDataTemplateView):
    """Returns a template to present all patrimonies."""
    template_name = 'geodata/geodata_bigmap.html'
    module = "bigmap"
    patrimonies = {
        'name': "Patrimonies",
        'external_graphic': settings.STATIC_URL+"img/patrimony.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url' : reverse_lazy('geojson_patrimony_list'),
    }
    constructions = {
        'name': "Constructions",
        'external_graphic': settings.STATIC_URL+"img/construction.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url' : reverse_lazy('geojson_construction_list'),
    }
    meetings = {
        'name': "Meetings",
        'external_graphic': settings.STATIC_URL+"img/meeting.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url' : reverse_lazy('geojson_meeting_list'),
    }
    actors = {
        'name': "Actors",
        'external_graphic' : settings.STATIC_URL+"img/actor.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url' : reverse_lazy('geojson_actor_list'),
    }
    map_layers = [patrimonies, constructions, meetings, actors]


class GeoDataDetailMixin(GeoDataMixin):
    def get_context_data(self, **kwargs):
        context = super(GeoDataDetailMixin, self).get_context_data(**kwargs)
        context['edit_geodata'] = self.edit_geodata
        context['delete_geodata'] = self.delete_geodata
        context['recommend_geodata'] = self.recommend_geodata
        return context


class GeoDataDetailView(GeoDataDetailMixin, DetailView):
    pass


class PatrimonyDetailView(GeoDataDetailView):
    """Returns a template to present one patrimony."""
    model = EarthGeoDataPatrimony
    context_object_name = 'geodata'
    module = "detail"
    patrimony = {
        'name': "Patrimony",
        'external_graphic' : settings.STATIC_URL+"img/patrimony.png",
        'graphic_width' : 20,
        'graphic_height' : 20,
        'fill_color' : '#00FF00',
        'stroke_color' : '#008800',
        'url' : 'geojson/',
    }
    map_layers = [patrimony]
    edit_geodata = 'edit_patrimony'
    delete_geodata = 'delete_patrimony'
    recommend_geodata = 'toggle_rec_patrimony'


class ConstructionDetailView(GeoDataDetailView):
    """Returns a template to present one construction."""
    model = EarthGeoDataConstruction
    context_object_name = 'geodata'
    module = "detail"
    construction = {
        'name': "Construction",
        'external_graphic' : settings.STATIC_URL+"img/construction.png",
        'graphic_width' : 20,
        'graphic_height' : 20,
        'fill_color' : '#00FF00',
        'stroke_color' : '#008800',
        'url' : 'geojson/',
    }
    map_layers = [construction]
    edit_geodata = 'edit_construction'
    delete_geodata = 'delete_construction'
    recommend_geodata = 'toggle_rec_construction'


class MeetingDetailView(GeoDataDetailView):
    """Returns a template to present one meeting."""
    model = EarthGeoDataMeeting
    context_object_name = 'geodata'
    module = "detail"
    meeting = {
        'name': "Meeting",
        'external_graphic' : settings.STATIC_URL+"img/meeting.png",
        'graphic_width' : 20,
        'graphic_height' : 20,
        'fill_color' : '#00FF00',
        'stroke_color' : '#008800',
        'url' : 'geojson/',
    }
    map_layers = [meeting]
    edit_geodata = 'edit_meeting'
    delete_geodata = 'delete_meeting'
    recommend_geodata = 'toggle_rec_meeting'


class ActorDetailView(GeoDataDetailView):
    """Returns a template to present one actor."""
    model = EarthGeoDataActor
    context_object_name = 'geodata'
    module = "detail"
    actor = {
        'name': "Actor",
        'external_graphic' : settings.STATIC_URL+"img/actor.png",
        'graphic_width' : 20,
        'graphic_height' : 20,
        'fill_color' : '#00FF00',
        'stroke_color' : '#008800',
        'url' : 'geojson/',
    }
    map_layers = [actor]
    edit_geodata = 'edit_actor'
    delete_geodata = 'delete_actor'
    recommend_geodata = 'toggle_rec_actor'



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


class OldBigMapView(TemplateView):
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


error_message = _("Please correct the errors below.")



class GeoDataCreateView(CreateView):
    context_object_name = 'geodata'
    template_name_suffix = '_add_form'

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.creator = self.request.user
        self.object.pub_date = now()
        messages.add_message(self.request, messages.SUCCESS,
                             _("Successfully added %(modelname)s \"%(name)s\".") %
                             { 'modelname': force_unicode(self.object._meta.verbose_name), 'name': self.object.name, }
                             )
        return super(GeoDataCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             error_message
                             )
        return super(GeoDataCreateView, self).form_invalid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GeoDataCreateView, self).dispatch(*args, **kwargs)


class PatrimonyCreateView(GeoDataCreateView):
    model = EarthGeoDataPatrimony
    form_class = EarthGeoDataPatrimonyForm


class ConstructionCreateView(GeoDataCreateView):
    model = EarthGeoDataConstruction
    form_class = EarthGeoDataConstructionForm


class MeetingCreateView(GeoDataCreateView):
    model = EarthGeoDataMeeting
    form_class = EarthGeoDataMeetingForm


class ActorCreateView(GeoDataCreateView):
    model = EarthGeoDataActor
    form_class = EarthGeoDataActorForm



class GeoDataUpdateView(UpdateView):
    context_object_name = 'geodata'
    template_name_suffix = '_edit_form'


    def get_object(self, *args, **kwargs):
        geodata = super(GeoDataUpdateView, self).get_object(*args, **kwargs)
        if geodata.creator != self.request.user:
            raise PermissionDenied
        else:
            return geodata

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS,
                             _("Successfully edited %(modelname)s \"%(name)s\".") %
                             { 'modelname': force_unicode(self.object._meta.verbose_name), 'name': self.object.name, }
                             )
        return super(GeoDataUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             error_message
                             )
        return super(GeoDataUpdateView, self).form_invalid(form)

    @method_decorator(login_required)
    #@method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(GeoDataUpdateView, self).dispatch(*args, **kwargs)


class PatrimonyUpdateView(GeoDataUpdateView):
    model = EarthGeoDataPatrimony
    form_class = EarthGeoDataPatrimonyForm
    template_name = 'edit_patrimony.html'


class ConstructionUpdateView(GeoDataUpdateView):
    model = EarthGeoDataConstruction
    form_class = EarthGeoDataConstructionForm
    template_name = 'edit_construction.html'


class MeetingUpdateView(GeoDataUpdateView):
    model = EarthGeoDataMeeting
    form_class = EarthGeoDataMeetingForm
    template_name = 'edit_meeting.html'


class ActorUpdateView(GeoDataUpdateView):
    model = EarthGeoDataActor
    form_class = EarthGeoDataActorForm
    template_name = 'edit_actor.html'


class GeoDataDeleteView(DeleteView):
    context_object_name = 'geodata'
    success_url = reverse_lazy('home')

    class Meta:
        abstract = True

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.add_message(request, messages.SUCCESS,
                             _("Successfully deleted %(modelname)s \"%(name)s\".") %
                             { 'modelname': force_unicode(self.object._meta.verbose_name),
                               'name': self.object.name, })
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        geodata = super(GeoDataDeleteView, self).get_object(*args, **kwargs)
        if geodata.creator != self.request.user:
            #messages.add_message(self.request, messages.ERROR,
            #                     _("You cannot delete %(modelname)s \"%(name)s\"") %
            #                     { 'modelname': force_unicode(geodata._meta.verbose_name),
            #                       'name': geodata.name, })
            raise PermissionDenied
        else:
            return geodata

    @method_decorator(login_required)
    #@method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(GeoDataDeleteView, self).dispatch(*args, **kwargs)


class PatrimonyDeleteView(GeoDataDeleteView):
    model = EarthGeoDataPatrimony
    form_class = EarthGeoDataPatrimonyForm


class ConstructionDeleteView(GeoDataDeleteView):
    model = EarthGeoDataConstruction
    form_class = EarthGeoDataConstructionForm


class MeetingDeleteView(GeoDataDeleteView):
    model = EarthGeoDataMeeting
    form_class = EarthGeoDataMeetingForm


class ActorDeleteView(GeoDataDeleteView):
    model = EarthGeoDataActor
    form_class = EarthGeoDataActorForm


class ToggleRecommendationView(SingleObjectMixin,View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = request.user.get_profile()
        if isinstance(self.object, EarthGeoDataPatrimony):
            recommendations = profile.r_patrimony 
        elif isinstance(self.object, EarthGeoDataConstruction):
            recommendations = profile.r_construction
        elif isinstance(self.object, EarthGeoDataMeeting):
            recommendations = profile.r_meeting
        elif isinstance(self.object, EarthGeoDataActor):
            recommendations = profile.r_actor
        else:
            raise ToggleRecommendationError

        if self.object in recommendations.all():
            recommendations.remove(self.object)
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully removed %(modelname)s \"%(name)s\" \
                             from your recommendations.") %
                                 { 'modelname': force_unicode(self.object._meta.verbose_name),
                                   'name': self.object.name, }
                                 )
        else:
            recommendations.add(self.object)
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully added %(modelname)s \"%(name)s\" \
                             to your recommendations.") %
                                 { 'modelname': force_unicode(self.object._meta.verbose_name),
                                   'name': self.object.name, }
                                 )
        #return HttpResponse('Success')
        return HttpResponseRedirect(self.object.get_absolute_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ToggleRecommendationView, self).dispatch(*args, **kwargs)


class ToggleRecommendationPatrimonyView(ToggleRecommendationView):
    model = EarthGeoDataPatrimony


class ToggleRecommendationConstructionView(ToggleRecommendationView):
    model = EarthGeoDataConstruction


class ToggleRecommendationMeetingView(ToggleRecommendationView):
    model = EarthGeoDataMeeting


class ToggleRecommendationActorView(ToggleRecommendationView):
    model = EarthGeoDataActor

