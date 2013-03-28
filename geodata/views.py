"""GeoData views."""

from django.utils.translation import ugettext_lazy as _
from models import EarthGeoDataPatrimony, EarthGeoDataConstruction,\
    EarthGeoDataMeeting, EarthGeoDataActor
from forms import EarthGeoDataPatrimonyForm, EarthGeoDataConstructionForm,\
    EarthGeoDataMeetingForm, EarthGeoDataActorForm, ImageFormSet
from sorl.thumbnail import get_thumbnail
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import SingleObjectMixin, DetailView,\
    BaseDetailView
from django.views.generic.list import ListView, BaseListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import json
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied


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
        data = {'crs':
                {
                    "type": "link",
                    "properties": {
                        "href": "http://spatialreference.org/ref/epsg/4326/",
                        "type": "proj4"}
                },
                'type': "Feature",
                'geometry': json.loads(m.geometry.geojson),
                'properties':
                {
                    'pk': m.pk, 'name': m.name,
                    'url': m.get_absolute_url(),
                    'image': get_thumbnail(m.image.all()[0].image, '100x100').url
                    if m.image.all() else None,
                }}
        return json.dumps(data)


class GeoJSONFeatureCollectionResponseMixin(GeoJSONResponseMixin):
    def convert_context_to_json(self, context):
        "Convert the context dictionary into a GeoJSON object"
        queryset = self.get_queryset()
        data = {'crs':
                {
                    "type": "link",
                    "properties": {
                        "href": "http://spatialreference.org/ref/epsg/4326/",
                        "type": "proj4"}
                },
                'type': "FeatureCollection",
                'features':
                [{'geometry': json.loads(m.geometry.geojson),
                  'type': "Feature",
                  'properties':
                  {
                      'pk': m.pk, 'name': m.name,
                      'url': m.get_absolute_url(),
                      'image': get_thumbnail(m.image.all()[0].image, '100x100').url
                      if m.image.all() else None,
                  }} for m in queryset]}
        return json.dumps(data)


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
        'external_graphic': settings.STATIC_URL + "img/patrimony.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [patrimonies]


class ConstructionListView(GeoDataListView):
    """Returns a template to present all constructions."""
    model = EarthGeoDataConstruction
    context_object_name = 'geodata'
    module = "list"
    constructions = {
        'name': "Constructions",
        'external_graphic': settings.STATIC_URL + "img/construction.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [constructions]


class MeetingListView(GeoDataListView):
    """Returns a template to present all meetings."""
    model = EarthGeoDataMeeting
    context_object_name = 'geodata'
    module = "list"
    meetings = {
        'name': "Meetings",
        'external_graphic': settings.STATIC_URL + "img/meeting.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [meetings]


class ActorListView(GeoDataListView):
    """Returns a template to present all actors."""
    model = EarthGeoDataActor
    context_object_name = 'geodata'
    module = "list"
    actors = {
        'name': "Actors",
        'external_graphic': settings.STATIC_URL + "img/actor.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
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
        'external_graphic': settings.STATIC_URL + "img/patrimony.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_patrimony_list'),
    }
    constructions = {
        'name': "Constructions",
        'external_graphic': settings.STATIC_URL + "img/construction.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_construction_list'),
    }
    meetings = {
        'name': "Meetings",
        'external_graphic': settings.STATIC_URL + "img/meeting.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_meeting_list'),
    }
    actors = {
        'name': "Actors",
        'external_graphic': settings.STATIC_URL + "img/actor.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_actor_list'),
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
        'external_graphic': settings.STATIC_URL + "img/patrimony.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
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
        'external_graphic': settings.STATIC_URL + "img/construction.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
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
        'external_graphic': settings.STATIC_URL + "img/meeting.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
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
        'external_graphic': settings.STATIC_URL + "img/actor.png",
        'graphic_width': 20,
        'graphic_height': 20,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [actor]
    edit_geodata = 'edit_actor'
    delete_geodata = 'delete_actor'
    recommend_geodata = 'toggle_rec_actor'


error_message = _("Please correct the errors below.")


class GeoDataCreateView(CreateView):
    context_object_name = 'geodata'
    template_name_suffix = '_add_form'

    def get_context_data(self, **kwargs):
        context = super(GeoDataCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST,
                                                    self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.pub_date = now()
        context = self.get_context_data()
        image_formset = context['image_formset']
        image_formset.instance = self.object
        if image_formset.is_valid():
            self.object.save()
            image_formset.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 _("Successfully added %(modelname)s \"%(name)s\".") %
                                 {'modelname': force_unicode(self.object._meta.verbose_name),
                                  'name': self.object.name, }
                                 )
            return HttpResponseRedirect(self.get_success_url())
            #return super(GeoDataCreateView, self).form_valid(form)
        else:
            self.form_invalid()

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

    def get_context_data(self, **kwargs):
        context = super(GeoDataUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST,
                                                    self.request.FILES,
                                                    instance=self.object)
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def get_object(self, *args, **kwargs):
        geodata = super(GeoDataUpdateView, self).get_object(*args, **kwargs)
        if geodata.creator == self.request.user or self.request.user.is_staff:
            return geodata
        else:
            raise PermissionDenied

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        image_formset = context['image_formset']
        #image_formset.instance = self.object
        if image_formset.is_valid():
            self.object.save()
            image_formset.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 _("Successfully edited %(modelname)s \"%(name)s\".") %
                                 {'modelname': force_unicode(self.object._meta.verbose_name),
                                  'name': self.object.name, }
                                 )
            return HttpResponseRedirect(self.get_success_url())
            #return super(GeoDataUpdateView, self).form_valid(form)
        else:
            self.form_invalid()

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
                             {'modelname': force_unicode(self.object._meta.verbose_name),
                              'name': self.object.name, })
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        geodata = super(GeoDataDeleteView, self).get_object(*args, **kwargs)
        if geodata.creator != self.request.user:
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


class ToggleRecommendationView(SingleObjectMixin, View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = request.user.profile
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
                                 {'modelname': force_unicode(self.object._meta.verbose_name),
                                  'name': self.object.name, }
                                 )
        else:
            recommendations.add(self.object)
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully added %(modelname)s \"%(name)s\" \
                             to your recommendations.") %
                                 {'modelname': force_unicode(self.object._meta.verbose_name),
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
