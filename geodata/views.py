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
from django.utils.text import Truncator


def _isceah(m):
    if hasattr(m, 'isceah'):
        return m.isceah
    else:
        return False


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
                    "type": "name",
                    "properties": {
                        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                    }
                },
                'type': "Feature",
                'geometry': json.loads(m.geometry.geojson),
                'properties':
                {
                    'pk': m.pk, 'name': m.name,
                    'url': m.get_absolute_url(),
                    'image': m.image.all()[0].thumbnail.url
                        if m.image.all() else None,
                    'summary':
                        Truncator(m.description).words(10, truncate=' [...]'),
                    'isceah': _isceah(m)
                }}
        return json.dumps(data)


class GeoJSONFeatureCollectionResponseMixin(GeoJSONResponseMixin):
    def convert_context_to_json(self, context):
        "Convert the context dictionary into a GeoJSON object"
        queryset = self.get_queryset()
        data = {'crs':
                {
                    "type": "name",
                    "properties": {
                        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                    }
                },
                'type': "FeatureCollection",
                'features':
                [{
                    'geometry': json.loads(m.geometry.geojson),
                    'type': "Feature",
                    'properties':
                    {
                        'pk': m.pk, 'name': m.name,
                        'url': m.get_absolute_url(),
                        'image': m.image.all()[0].thumbnail.url
                            if m.image.all() else None,
                        'summary': Truncator(m.description).words(
                            10, truncate=' [...]'
                        ),
                        'isceah': _isceah(m)
                    }
                } for m in queryset]}
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
    geodata_detail_url = "show_building"
    geodata_list_url = "show_building_all"
    geodata_add_url = "add_building"
    geodata_edit_url = "edit_building"
    geodata_delete_url = "delete_building"
    geodata_recommend_url = "toggle_rec_building"


class WorksiteMixin(object):
    geodata_detail_url = "show_worksite"
    geodata_list_url = "show_worksite_all"
    geodata_add_url = "add_worksite"
    geodata_edit_url = "edit_worksite"
    geodata_delete_url = "delete_worksite"
    geodata_recommend_url = "toggle_rec_worksite"


class EventMixin(object):
    geodata_detail_url = "show_event"
    geodata_list_url = "show_event_all"
    geodata_add_url = "add_event"
    geodata_edit_url = "edit_event"
    geodata_delete_url = "delete_event"
    geodata_recommend_url = "toggle_rec_event"


class StakeholderMixin(object):
    geodata_detail_url = "show_stakeholder"
    geodata_list_url = "show_stakeholder_all"
    geodata_add_url = "add_stakeholder"
    geodata_edit_url = "edit_stakeholder"
    geodata_delete_url = "delete_stakeholder"
    geodata_recommend_url = "toggle_rec_stakeholder"


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
    """Returns a template to present all buildings."""
    model = Building
    buildings = {
        'name': "Buildings",
        'external_graphic': settings.STATIC_URL + "img/building_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [buildings]


class WorksiteListView(WorksiteMixin, GeoDataListView):
    """Returns a template to present all worksites."""
    model = Worksite
    worksites = {
        'name': "Worksites",
        'external_graphic': settings.STATIC_URL + "img/worksite_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [worksites]


class EventListView(EventMixin, GeoDataListView):
    """Returns a template to present all events."""
    model = Event
    events = {
        'name': "Events",
        'external_graphic': settings.STATIC_URL + "img/event_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [events]

    def get_queryset(self):
        queryset = super(EventListView, self).get_queryset()
        event_type = self.kwargs.get('type', None)
        if event_type:
            return queryset.filter(event_type__ident_name__iexact=event_type)
        else:
            return queryset


class StakeholderListView(StakeholderMixin, GeoDataListView):
    """Returns a template to present all stakeholders."""
    model = Stakeholder
    stakeholders = {
        'name': "Stakeholders",
        'external_graphic': settings.STATIC_URL + "img/stakeholder_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [stakeholders]

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
    """Returns a template to present all buildings."""
    template_name = 'geodata/geodata_bigmap.html'
    module = "bigmap"
    buildings = {
        'name': "Buildings",
        'external_graphic': settings.STATIC_URL + "img/building_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_building_list'),
    }
    worksites = {
        'name': "Worksites",
        'external_graphic': settings.STATIC_URL + "img/worksite_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_worksite_list'),
    }
    events = {
        'name': "Events",
        'external_graphic': settings.STATIC_URL + "img/event_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_event_list'),
    }
    stakeholders = {
        'name': "Stakeholders",
        'external_graphic': settings.STATIC_URL + "img/stakeholder_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': reverse_lazy('geojson_stakeholder_list'),
    }
    map_layers = [buildings, worksites, events, stakeholders]


class GeoDataSingleObjectMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GeoDataSingleObjectMixin,
                        self).get_context_data(**kwargs)
        # object = self.get_object()
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
    """Returns a template to present one building."""
    model = Building
    building = {
        'name': "Building",
        'external_graphic': settings.STATIC_URL + "img/building_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [building]


class WorksiteDetailView(WorksiteMixin, GeoDataDetailView):
    """Returns a template to present one worksite."""
    model = Worksite
    worksite = {
        'name': "Worksite",
        'external_graphic': settings.STATIC_URL + "img/worksite_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [worksite]


class EventDetailView(EventMixin, GeoDataDetailView):
    """Returns a template to present one event."""
    model = Event
    event = {
        'name': "Event",
        'external_graphic': settings.STATIC_URL + "img/event_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [event]


class StakeholderDetailView(StakeholderMixin, GeoDataDetailView):
    """Returns a template to present one stakeholder."""
    model = Stakeholder
    stakeholders = {
        'name': "Stakeholders",
        'external_graphic': settings.STATIC_URL + "img/stakeholder_icon_h25.png",
        'graphic_width': 10,
        'graphic_height': 10,
        'fill_color': '#00FF00',
        'stroke_color': '#008800',
        'url': 'geojson/',
    }
    map_layers = [stakeholders]


error_message = _("Please correct the errors below.")


class UserFormViewMixin(object):
    def get_form_kwargs(self):
        kwargs = super(UserFormViewMixin, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class GeoDataCreateView(GeoDataSingleObjectMixin, GeoDataMixin,
                        UserFormViewMixin, CreateView):
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
            form.save_m2m()
            image_formset.save()
            messages.add_message(
                self.request, messages.SUCCESS,
                _("Successfully added %(modelname)s \"%(name)s\".") %
                {'modelname': force_unicode(self.object._meta.verbose_name),
                 'name': self.object.name, }
            )
            return HttpResponseRedirect(self.get_success_url())
            # return super(GeoDataCreateView, self).form_valid(form)
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


class GeoDataUpdateView(GeoDataSingleObjectMixin, GeoDataMixin,
                        UserFormViewMixin, UpdateView):
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
        # image_formset.instance = self.object
        if image_formset.is_valid():
            self.object.save()
            form.save_m2m()
            image_formset.save()
            messages.add_message(
                self.request, messages.SUCCESS,
                _("Successfully edited %(modelname)s \"%(name)s\".") %
                {'modelname': force_unicode(self.object._meta.verbose_name),
                 'name': self.object.name, }
            )
            return HttpResponseRedirect(self.get_success_url())
            # return super(GeoDataUpdateView, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             error_message
                             )
        return super(GeoDataUpdateView, self).form_invalid(form)

    @method_decorator(login_required)
    # @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(GeoDataUpdateView, self).dispatch(*args, **kwargs)


class BuildingUpdateView(BuildingMixin, GeoDataUpdateView):
    model = Building
    form_class = BuildingForm


class WorksiteUpdateView(WorksiteMixin, GeoDataUpdateView):
    model = Worksite
    form_class = WorksiteForm


class EventUpdateView(EventMixin, GeoDataUpdateView):
    model = Event
    form_class = EventForm


class StakeholderUpdateView(StakeholderMixin, GeoDataUpdateView):
    model = Stakeholder
    form_class = StakeholderForm


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
    # @method_decorator(user_passes_test(lambda u: u.is_staff))
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
        # return HttpResponse('Success')
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
        return queryset.filter(id__in=profile.r_building.all())


class GeoJSONProfileRecommendWorksiteListView(
        GeoJSONProfileRecommendListView):
    model = Worksite

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendWorksiteListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_worksite.all())


class GeoJSONProfileRecommendEventListView(GeoJSONProfileRecommendListView):
    model = Event

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendEventListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_event.all())


class GeoJSONProfileRecommendStakeholderListView(
    GeoJSONProfileRecommendListView
):
    model = Stakeholder

    def get_queryset(self, **kwargs):
        queryset = super(GeoJSONProfileRecommendStakeholderListView,
                         self).get_queryset(**kwargs)
        profile = self.get_profile()
        return queryset.filter(id__in=profile.r_stakeholder.all())


class ProfileDetailView(DetailView):
    """Returns a template to present all buildings of a given profile."""
    # template_name = 'profilemap.html'
    module = "profilemap"
    model = Profile
    slug_field = 'user__username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)

        profile = get_object_or_404(Profile,
                                    user__username=self.kwargs['slug'])
        username = profile.user.username

        buildings = {
            'name': "Buildings %s" % username,
            'external_graphic': settings.STATIC_URL +
            "img/building_icon_h25.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_building',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        worksites = {
            'name': "Worksites %s" % username,
            'external_graphic': settings.STATIC_URL +
            "img/worksite_icon_h25.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_worksite',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        events = {
            'name': "Events %s" % username,
            'external_graphic': settings.STATIC_URL + "img/event_icon_h25.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_event',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        stakeholders = {
            'name': "Stakeholdrs %s" % username,
            'external_graphic': settings.STATIC_URL +
            "img/stakeholder_icon_h25.png",
            'graphic_width': 20,
            'graphic_height': 20,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_creator_stakeholder',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_buildings = {
            'name': "Recommendations %s: Buildings" % username,
            'external_graphic': settings.STATIC_URL + "img/building_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_building',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_worksites = {
            'name': "Recommendations %s: Worksites" % username,
            'external_graphic': settings.STATIC_URL + "img/worksite_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_worksite',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_events = {
            'name': "Recommendations %s: Events" % username,
            'external_graphic': settings.STATIC_URL + "img/event_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_event',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        recommendations_stakeholders = {
            'name': "Recommendations %s: Stakeholders" % username,
            'external_graphic': settings.STATIC_URL +
            "img/stakeholder_dot.png",
            'graphic_width': 10,
            'graphic_height': 10,
            'fill_color': '#00FF00',
            'stroke_color': '#008800',
            'url': reverse_lazy('geojson_profile_recommend_stakeholder',
                                kwargs={'slug': self.kwargs['slug']}),
        }
        context['map_layers'] = [buildings, worksites, events, stakeholders,
                                 recommendations_buildings,
                                 recommendations_worksites,
                                 recommendations_events,
                                 recommendations_stakeholders]
        context['module'] = self.module
        return context


class ProfileListView(ListView):
    """Returns a template to present all profiles."""
    model = Profile
    # template_name = 'profile_list.html'
