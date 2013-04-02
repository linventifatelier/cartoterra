"""urls file."""

from django.conf.urls import patterns, url
from geodata import models
from geodata import views
from geodata import feeds
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q


urlpatterns = patterns(
    '',
    url(r'^feeds/patrimony/$', feeds.BuildingFeed(), name="feed_patrimony"),
    url(r'^feeds/construction/$', feeds.WorksiteFeed(),
        name="feed_construction"),
    url(r'^feeds/meeting/$', feeds.EventFeed(), name="feed_meeting"),
    url(r'^feeds/actor/$', feeds.StakeholderFeed(), name="feed_actor"),
    url(r'^patrimony/(?P<pk>\d+)/geojson/$',
        views.GeoJSONBuildingDetailView.as_view(),
        name="geojson_patrimony_detail"),
    url(r'^construction/(?P<pk>\d+)/geojson/$',
        views.GeoJSONWorksiteDetailView.as_view(),
        name="geojson_construction_detail"),
    url(r'^meeting/(?P<pk>\d+)/geojson/$',
        views.GeoJSONEventDetailView.as_view(),
        name="geojson_meeting_detail"),
    url(r'^actor/(?P<pk>\d+)/geojson/$',
        views.GeoJSONStakeholderDetailView.as_view(),
        name="geojson_actor_detail"),
    url(r'^patrimony/all/geojson/$', views.GeoJSONBuildingListView.as_view(),
        name="geojson_patrimony_list"),
    url(r'^patrimony/contemporary/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(
                inauguration_date__gte=now() - timedelta(days=3650)))),
    url(r'^patrimony/unesco/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(unesco=True))),
    url(r'^patrimony/vernacular/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(architects=''))),
    url(r'^patrimony/normal/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.exclude(architects='').filter(
                Q(unesco=False) &
                (Q(inauguration_date__isnull=True) |
                 ~Q(inauguration_date__gte=now() - timedelta(days=3650)))))),
    url(r'^construction/all/geojson/$',
        views.GeoJSONWorksiteListView.as_view(),
        name="geojson_construction_list"),
    url(r'^construction/participative/geojson/$',
        views.GeoJSONWorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=True))),
    url(r'^construction/normal/geojson/$',
        views.GeoJSONWorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=False))),
    url(r'^meeting/all/geojson/$', views.GeoJSONEventListView.as_view(),
        name="geojson_meeting_list"),
    url(r'^meeting/type/(?P<type>[a-zA-Z0-9_\-]+)/geojson/$',
        views.GeoJSONEventListView.as_view(),
        name="geojson_event_of_type"),
    url(r'^actor/all/geojson/$', views.GeoJSONStakeholderListView.as_view(),
        name="geojson_actor_list"),
    url(r'^actor/role/(?P<role>[a-zA-Z0-9_\-]+)/geojson/$',
        views.GeoJSONStakeholderListView.as_view(),
        name="geojson_stakeholder_of_role"),
    url(r'^patrimony/all/$', views.BuildingListView.as_view(),
        name="show_patrimony_all"),
    url(r'^patrimony/contemporary/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(
                inauguration_date__gte=now() - timedelta(days=3650))),
        name="show_patrimony_contemporary"),
    url(r'^patrimony/unesco/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(unesco=True)),
        name="show_patrimony_unesco"),
    url(r'^patrimony/vernacular/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(architects='')),
        name="show_patrimony_vernacular"),
    url(r'^patrimony/normal/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.exclude(architects='').filter(
                Q(unesco=False) &
                (Q(inauguration_date__isnull=True) |
                 ~Q(inauguration_date__gte=now() - timedelta(days=3650))))),
        name="show_patrimony_normal"),
    url(r'^patrimony/(?P<pk>\d+)/$', views.BuildingDetailView.as_view(),
        name="show_patrimony"),
    url(r'^construction/all/$', views.WorksiteListView.as_view(),
        name="show_construction_all"),
    url(r'^construction/participative/$',
        views.WorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=True)),
        name="show_construction_participative"),
    url(r'^construction/normal/$',
        views.WorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=False)),
        name="show_construction_normal"),
    url(r'^construction/(?P<pk>\d+)/$', views.WorksiteDetailView.as_view(),
        name="show_construction"),
    url(r'^meeting/all/$', views.EventListView.as_view(),
        name="show_meeting_all"),
    url(r'^meeting/type/(?P<type>[a-zA-Z0-9_\-]+)/$',
        views.EventListView.as_view(),
        name="show_event_of_type"),
    url(r'^meeting/(?P<pk>\d+)/$', views.EventDetailView.as_view(),
        name="show_meeting"),
    url(r'^actor/all/$', views.StakeholderListView.as_view(),
        name="show_actor_all"),
    url(r'^actor/role/(?P<role>[a-zA-Z0-9_\-]+)/$',
        views.StakeholderListView.as_view(),
        name="show_stakeholder_of_role"),
    url(r'^actor/(?P<pk>\d+)/$', views.StakeholderDetailView.as_view(),
        name="show_actor"),
    url(r'^patrimony/(?P<pk>\d+)/edit/$', views.BuildingUpdateView.as_view(),
        name="edit_patrimony"),
    url(r'^construction/(?P<pk>\d+)/edit/$',
        views.WorksiteUpdateView.as_view(), name="edit_construction"),
    url(r'^meeting/(?P<pk>\d+)/edit/$', views.EventUpdateView.as_view(),
        name="edit_meeting"),
    url(r'^actor/(?P<pk>\d+)/edit/$', views.StakeholderUpdateView.as_view(),
        name="edit_actor"),
    url(r'^patrimony/(?P<pk>\d+)/delete/$',
        views.BuildingDeleteView.as_view(), name="delete_patrimony"),
    url(r'^construction/(?P<pk>\d+)/delete/$',
        views.WorksiteDeleteView.as_view(), name="delete_construction"),
    url(r'^meeting/(?P<pk>\d+)/delete/$', views.EventDeleteView.as_view(),
        name="delete_meeting"),
    url(r'^actor/(?P<pk>\d+)/delete/$', views.StakeholderDeleteView.as_view(),
        name="delete_actor"),
    url(r'^patrimony/add/$', views.BuildingCreateView.as_view(),
        name="add_patrimony"),
    url(r'^construction/add/$', views.WorksiteCreateView.as_view(),
        name="add_construction"),
    url(r'^meeting/add/$', views.EventCreateView.as_view(),
        name="add_meeting"),
    url(r'^actor/add/$', views.StakeholderCreateView.as_view(),
        name="add_actor"),
    url(r'^patrimony/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationBuildingView.as_view(),
        name="toggle_rec_patrimony"),
    url(r'^construction/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationWorksiteView.as_view(),
        name="toggle_rec_construction"),
    url(r'^meeting/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationEventView.as_view(),
        name="toggle_rec_meeting"),
    url(r'^actor/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationStakeholderView.as_view(),
        name="toggle_rec_actor"),
    url(r'^all/$', views.BigMapView.as_view(),
        name="show_bigmap"),
)
