"""GeoData views."""

from django.utils.translation import ugettext_lazy as _
from models import Building, Worksite, Event, Stakeholder, Profile
from forms import BuildingForm, WorksiteForm, EventForm, StakeholderForm, \
    ImageFormSet
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
from django.shortcuts import get_object_or_404


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
                    'image': m.image.all()[0].thumbnail.url
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
                      'image': m.image.all()[0].thumbnail.url
                      if m.image.all() else None,
                  }} for m in queryset]}
        return json.dumps(data)


class GeoJSONDetailView(GeoJSONFeatureResponseMixin, BaseDetailView):
    pass


class GeoJSONListView(GeoJSONFeatureCollectionResponseMixin, BaseListView):
    pass


class GeoJSONBuildingListView(GeoJSONListView):
    model = Building


class GeoJSONBuildingDetailView(GeoJSONDetailView):
    model = Building


class GeoJSONWorksiteListView(GeoJSONListView):
    model = Worksite


class GeoJSONWorksiteDetailView(GeoJSONDetailView):
    model = Worksite


class GeoJSONEventListView(GeoJSONListView):
    model = Event

    def get_queryset(self):
        queryset = super(GeoJSONEventListView, self).get_queryset()
        event_type = self.kwargs.get('event_type', None)
        if event_type:
            return queryset.filter(event_type__ident_name__iexact=event_type)
        else:
            return queryset


class GeoJSONEventDetailView(GeoJSONDetailView):
    model = Event


class GeoJSONStakeholderListView(GeoJSONListView):
    model = Stakeholder

    def get_queryset(self):
        queryset = super(GeoJSONStakeholderListView, self).get_queryset()
        role = self.kwargs.get('role', None)
        if role:
            return queryset.filter(role__ident_name__iexact=role)
        else:
            return queryset


class GeoJSONStakeholderDetailView(GeoJSONDetailView):
    model = Stakeholder


class GeoDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GeoDataMixin, self).get_context_data(**kwargs)
        context['geodata_detail_url'] = self.geodata_detail_url
        context['geodata_list_url'] = self.geodata_list_url
        context['geodata_add_url'] = self.geodata_add_url
        context['geodata_edit_url'] = self.geodata_edit_url
        context['geodata_delete_url'] = self.geodata_delete_url
        context['geodata_recommend_url'] = self.geodata_recommend_url
        return context


class BuildingMixin(object):
    geodata_detail_url = "show_patrimony"
    geodata_list_url = "show_patrimony_all"
    geodata_add_url = "add_patrimony"
    geodata_edit_url = "edit_patrimony"
    geodata_delete_url = "delete_patrimony"
    geodata_recommend_url = "toggle_rec_patrimony"


class WorksiteMixin(object):
    geodata_detail_url = "show_construction"
    geodata_list_url = "show_construction_all"
    geodata_add_url = "add_construction"
    geodata_edit_url = "edit_construction"
    geodata_delete_url = "delete_construction"
    geodata_recommend_url = "toggle_rec_construction"


class EventMixin(object):
    geodata_detail_url = "show_meeting"
    geodata_list_url = "show_meeting_all"
    geodata_add_url = "add_meeting"
    geodata_edit_url = "edit_meeting"
    geodata_delete_url = "delete_meeting"
    geodata_recommend_url = "toggle_rec_meeting"


class StakeholderMixin(object):
    geodata_detail_url = "show_actor"
    geodata_list_url = "show_actor_all"
    geodata_add_url = "add_actor"
    geodata_edit_url = "edit_actor"
    geodata_delete_url = "delete_actor"
    geodata_recommend_url = "toggle_rec_actor"


class GeoDataMapMixin(GeoDataMixin):
    def get_context_data(self, **kwargs):
        context = super(GeoDataMapMixin, self).get_context_data(**kwargs)
        context['module'] = self.module
        context['map_layers'] = self.map_layers
        return context


class GeoDataMultipleObjectsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GeoDataMultipleObjectsMixin,
                        self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['geodata_verbose_name'] = \
            queryset.model._meta.verbose_name.title()
        context['geodata_verbose_name_plural'] = \
            queryset.model._meta.verbose_name_plural.title()
        return context


class GeoDataListView(GeoDataMultipleObjectsMixin, GeoDataMapMixin, ListView):
    context_object_name = 'geodata'
    module = "list"
    pass


class BuildingListView(BuildingMixin, GeoDataListView):
    """Returns a template to present all patrimonies."""
    model = Building
    patrimonies = {
        'name': "Patrimonies",
        'external_graphic': settings.STATIC_URL + "img/building_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [patrimonies]


class WorksiteListView(WorksiteMixin, GeoDataListView):
    """Returns a template to present all constructions."""
    model = Worksite
    constructions = {
        'name': "Constructions",
        'external_graphic': settings.STATIC_URL + "img/construction_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [constructions]


class EventListView(EventMixin, GeoDataListView):
    """Returns a template to present all meetings."""
    model = Event
    meetings = {
        'name': "Meetings",
        'external_graphic': settings.STATIC_URL + "img/event_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [meetings]

    def get_queryset(self):
        queryset = super(EventListView, self).get_queryset()
        event_type = self.kwargs.get('type', None)
        if event_type:
            return queryset.filter(event_type__ident_name__iexact=event_type)
        else:
            return queryset


class StakeholderListView(StakeholderMixin, GeoDataListView):
    """Returns a template to present all actors."""
    model = Stakeholder
    actors = {
        'name': "Actors",
        'external_graphic': settings.STATIC_URL + "img/stakeholder_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [actors]

    def get_queryset(self):
        queryset = super(StakeholderListView, self).get_queryset()
        role = self.kwargs.get('role', None)
        if role:
            return queryset.filter(role__ident_name__iexact=role)
        else:
            return queryset


class GeoDataAllMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GeoDataAllMixin, self).get_context_data(**kwargs)
        context['module'] = self.module
        context['map_layers'] = self.map_layers
        return context


class GeoDataAllView(GeoDataAllMixin, TemplateView):
    pass


class BigMapView(GeoDataAllView):
    """Returns a template to present all patrimonies."""
    template_name = 'geodata/geodata_bigmap.html'
    module = "bigmap"
    patrimonies = {
        'name': "Patrimonies",
        'external_graphic': settings.STATIC_URL + "img/building_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_patrimony_list'),
    }
    constructions = {
        'name': "Constructions",
        'external_graphic': settings.STATIC_URL + "img/construction_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_construction_list'),
    }
    meetings = {
        'name': "Meetings",
        'external_graphic': settings.STATIC_URL + "img/event_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_meeting_list'),
    }
    actors = {
        'name': "Actors",
        'external_graphic': settings.STATIC_URL + "img/stakeholder_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_actor_list'),
    }
    map_layers = [patrimonies, constructions, meetings, actors]


class GeoDataSingleObjectMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GeoDataSingleObjectMixin,
                        self).get_context_data(**kwargs)
        #object = self.get_object()
        context['geodata_verbose_name'] = self.model._meta.verbose_name.title()
        context['geodata_verbose_name_plural'] = \
            self.model._meta.verbose_name_plural.title()
        return context


class GeoDataDetailMixin(GeoDataSingleObjectMixin, GeoDataMapMixin):
    def get_context_data(self, **kwargs):
        context = super(GeoDataDetailMixin, self).get_context_data(**kwargs)
        return context


class GeoDataDetailView(GeoDataDetailMixin, DetailView):
    context_object_name = 'geodata'
    module = "detail"
    pass


class BuildingDetailView(BuildingMixin, GeoDataDetailView):
    """Returns a template to present one patrimony."""
    model = Building
    patrimony = {
        'name': "Patrimony",
        'external_graphic': settings.STATIC_URL + "img/building_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [patrimony]


class WorksiteDetailView(WorksiteMixin, GeoDataDetailView):
    """Returns a template to present one construction."""
    model = Worksite
    construction = {
        'name': "Construction",
        'external_graphic': settings.STATIC_URL + "img/construction_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [construction]


class EventDetailView(EventMixin, GeoDataDetailView):
    """Returns a template to present one meeting."""
    model = Event
    meeting = {
        'name': "Meeting",
        'external_graphic': settings.STATIC_URL + "img/event_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [meeting]


class StakeholderDetailView(StakeholderMixin, GeoDataDetailView):
    """Returns a template to present one actor."""
    model = Stakeholder
    actor = {
        'name': "Actor",
        'external_graphic': settings.STATIC_URL + "img/stakeholder_dot.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [actor]


error_message = _("Please correct the errors below.")


class GeoDataCreateView(GeoDataSingleObjectMixin, GeoDataMixin, CreateView):
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
            messages.add_message(
                self.request, messages.SUCCESS,
                _("Successfully added %(modelname)s \"%(name)s\".") %
                {'modelname': force_unicode(self.object._meta.verbose_name),
                 'name': self.object.name, }
            )
            return HttpResponseRedirect(self.get_success_url())
            #return super(GeoDataCreateView, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             error_message
                             )
        return super(GeoDataCreateView, self).form_invalid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GeoDataCreateView, self).dispatch(*args, **kwargs)


class BuildingCreateView(BuildingMixin, GeoDataCreateView):
    model = Building
    form_class = BuildingForm


class WorksiteCreateView(WorksiteMixin, GeoDataCreateView):
    model = Worksite
    form_class = WorksiteForm


class EventCreateView(EventMixin, GeoDataCreateView):
    model = Event
    form_class = EventForm


class StakeholderCreateView(StakeholderMixin, GeoDataCreateView):
    model = Stakeholder
    form_class = StakeholderForm


class GeoDataUpdateView(GeoDataSingleObjectMixin, GeoDataMixin, UpdateView):
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
            messages.add_message(
                self.request, messages.SUCCESS,
                _("Successfully edited %(modelname)s \"%(name)s\".") %
                {'modelname': force_unicode(self.object._meta.verbose_name),
                 'name': self.object.name, }
            )
            return HttpResponseRedirect(self.get_success_url())
            #return super(GeoDataUpdateView, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             error_message
                             )
        return super(GeoDataUpdateView, self).form_invalid(form)

    @method_decorator(login_required)
    #@method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(GeoDataUpdateView, self).dispatch(*args, **kwargs)


class BuildingUpdateView(BuildingMixin, GeoDataUpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'edit_patrimony.html'


class WorksiteUpdateView(WorksiteMixin, GeoDataUpdateView):
    model = Worksite
    form_class = WorksiteForm
    template_name = 'edit_construction.html'


class EventUpdateView(EventMixin, GeoDataUpdateView):
    model = Event
    form_class = EventForm
    template_name = 'edit_meeting.html'


class StakeholderUpdateView(StakeholderMixin, GeoDataUpdateView):
    model = Stakeholder
    form_class = StakeholderForm
    template_name = 'edit_actor.html'


class GeoDataDeleteView(GeoDataSingleObjectMixin, GeoDataMixin, DeleteView):
    context_object_name = 'geodata'
    success_url = reverse_lazy('home')

    class Meta:
        abstract = True

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.add_message(
            request, messages.SUCCESS,
            _("Successfully deleted %(modelname)s \"%(name)s\".") %
            {'modelname': force_unicode(self.object._meta.verbose_name),
             'name': self.object.name, }
        )
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


class BuildingDeleteView(BuildingMixin, GeoDataDeleteView):
    model = Building
    form_class = BuildingForm


class WorksiteDeleteView(WorksiteMixin, GeoDataDeleteView):
    model = Worksite
    form_class = WorksiteForm


class EventDeleteView(EventMixin, GeoDataDeleteView):
    model = Event
    form_class = EventForm


class StakeholderDeleteView(StakeholderMixin, GeoDataDeleteView):
    model = Stakeholder
    form_class = StakeholderForm


class GeoDataError(Exception):
    pass


class ToggleRecommendationView(SingleObjectMixin, View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = request.user.profile
        if isinstance(self.object, Building):
            recommendations = profile.r_building
        elif isinstance(self.object, Worksite):
            recommendations = profile.r_worksite
        elif isinstance(self.object, Event):
            recommendations = profile.r_event
        elif isinstance(self.object, Stakeholder):
            recommendations = profile.r_stakeholder
        else:
            raise GeoDataError

        if self.object in recommendations.all():
            recommendations.remove(self.object)
            profile.save()
            messages.add_message(
                request, messages.SUCCESS,
                _("Successfully removed %(modelname)s \"%(name)s\" from your \
                recommendations.") %
                {'modelname': force_unicode(self.object._meta.verbose_name),
                 'name': self.object.name, }
            )
        else:
            recommendations.add(self.object)
            profile.save()
            messages.add_message(
                request, messages.SUCCESS,
                _("Successfully added %(modelname)s \"%(name)s\" to your \
                recommendations.") %
                {'modelname': force_unicode(self.object._meta.verbose_name),
                 'name': self.object.name, }
            )
        #return HttpResponse('Success')
        return HttpResponseRedirect(self.object.get_absolute_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ToggleRecommendationView, self).dispatch(*args, **kwargs)


class ToggleRecommendationBuildingView(ToggleRecommendationView):
    model = Building


class ToggleRecommendationWorksiteView(ToggleRecommendationView):
    model = Worksite


class ToggleRecommendationEventView(ToggleRecommendationView):
    model = Event


class ToggleRecommendationStakeholderView(ToggleRecommendationView):
    model = Stakeholder


class GeoJSONProfileCreatorMixin(GeoJSONFeatureCollectionResponseMixin):
    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileCreatorMixin,
                         self).get_queryset(**kwargs)
        return queryset.filter(creator__username=self.kwargs['slug'])


class GeoJSONProfileCreatorListView(GeoJSONProfileCreatorMixin, BaseListView):
    pass


class GeoJSONProfileCreatorBuildingListView(GeoJSONProfileCreatorListView):
    model = Building


class GeoJSONProfileCreatorWorksiteListView(GeoJSONProfileCreatorListView):
    model = Worksite


class GeoJSONProfileCreatorEventListView(GeoJSONProfileCreatorListView):
    model = Event


class GeoJSONProfileCreatorStakeholderListView(GeoJSONProfileCreatorListView):
    model = Stakeholder


class GeoJSONProfileRecommendListView(GeoJSONListView):
    def get_profile(self, **kwargs):
        return get_object_or_404(Profile, user__username=self.kwargs['slug'])


class GeoJSONProfileRecommendBuildingListView(
        GeoJSONProfileRecommendListView):
    model = Building

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendBuildingListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_patrimony.all())


class GeoJSONProfileRecommendWorksiteListView(
        GeoJSONProfileRecommendListView):
    model = Worksite

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendWorksiteListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_construction.all())


class GeoJSONProfileRecommendEventListView(GeoJSONProfileRecommendListView):
    model = Event

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendEventListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_meeting.all())


class GeoJSONProfileRecommendStakeholderListView(
    GeoJSONProfileRecommendListView
):
    model = Stakeholder

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendStakeholderListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_actor.all())


class ProfileDetailView(DetailView):
    """Returns a template to present all patrimonies of a given profile."""
    #template_name = 'profilemap.html'
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
    #template_name = 'profile_list.html'
