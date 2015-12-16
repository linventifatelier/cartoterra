"""urls file."""

from django.conf.urls import url
from geodata import models
from geodata import views
from geodata import feeds
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q


urlpatterns = [
    url(r'^feeds/building/$', feeds.BuildingFeed(), name="feed_building"),
    url(r'^feeds/worksite/$', feeds.WorksiteFeed(),
        name="feed_worksite"),
    url(r'^feeds/event/$', feeds.EventFeed(), name="feed_event"),
    url(r'^feeds/people/$', feeds.StakeholderFeed(), name="feed_stakeholder"),
    url(r'^building/(?P<pk>\d+)/geojson/$',
        views.GeoJSONBuildingDetailView.as_view(),
        name="geojson_building_detail"),
    url(r'^worksite/(?P<pk>\d+)/geojson/$',
        views.GeoJSONWorksiteDetailView.as_view(),
        name="geojson_worksite_detail"),
    url(r'^event/(?P<pk>\d+)/geojson/$',
        views.GeoJSONEventDetailView.as_view(),
        name="geojson_event_detail"),
    url(r'^people/(?P<pk>\d+)/geojson/$',
        views.GeoJSONStakeholderDetailView.as_view(),
        name="geojson_stakeholder_detail"),
    url(r'^building/all/geojson/$', views.GeoJSONBuildingListView.as_view(),
        name="geojson_building_list"),
    url(r'^building/status/(?P<status>[a-zA-Z0-9_\-]+)/geojson/$',
        views.GeoJSONBuildingListView.as_view(),
        name="geojson_building_of_status"),
    url(r'^building/contemporary/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(
                inauguration_date__gte=now() - timedelta(days=3650)))),
    url(r'^building/isceah/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(isceah=True))),
    url(r'^building/isceah/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(isceah=True)),
        name="show_building_isceah"),
    url(r'^building/unesco/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(unesco=True))),
    url(r'^building/vernacular/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(architects=''))),
    url(r'^building/normal/geojson/$',
        views.GeoJSONBuildingListView.as_view(
            queryset=models.Building.objects.filter(
                Q(unesco=False) &
                Q(isceah=False) &
                Q(construction_status__isnull=True)))),
    url(r'^worksite/all/geojson/$',
        views.GeoJSONWorksiteListView.as_view(),
        name="geojson_worksite_list"),
    url(r'^worksite/participative/geojson/$',
        views.GeoJSONWorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=True))),
    url(r'^worksite/normal/geojson/$',
        views.GeoJSONWorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=False))),
    url(r'^event/all/geojson/$', views.GeoJSONEventListView.as_view(),
        name="geojson_event_list"),
    url(r'^event/type/(?P<type>[a-zA-Z0-9_\-]+)/geojson/$',
        views.GeoJSONEventListView.as_view(),
        name="geojson_event_of_type"),
    url(r'^people/all/geojson/$', views.GeoJSONStakeholderListView.as_view(),
        name="geojson_stakeholder_list"),
    url(r'^people/role/(?P<role>[a-zA-Z0-9_\-]+)/geojson/$',
        views.GeoJSONStakeholderListView.as_view(),
        name="geojson_stakeholder_of_role"),
    url(r'^people/isceah/$',
        views.StakeholderListView.as_view(
            queryset=models.Stakeholder.objects.filter(isceah=True)),
        name="show_stakeholder_isceah"),
    url(r'^people/isceah/geojson/$',
        views.GeoJSONStakeholderListView.as_view(
            queryset=models.Stakeholder.objects.filter(isceah=True))),
    url(r'^building/all/$', views.BuildingListView.as_view(),
        name="show_building_all"),
    url(r'^building/status/(?P<status>[a-zA-Z0-9_\-]+)/$',
        views.BuildingListView.as_view(),
        name="show_building_of_status"),
    url(r'^building/contemporary/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(
                inauguration_date__gte=now() - timedelta(days=3650))),
        name="show_building_contemporary"),
    url(r'^building/unesco/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(unesco=True)),
        name="show_building_unesco"),
    url(r'^building/vernacular/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(architects='')),
        name="show_building_vernacular"),
    url(r'^building/normal/$',
        views.BuildingListView.as_view(
            queryset=models.Building.objects.filter(
                Q(unesco=False) &
                Q(isceah=False) &
                Q(construction_status__isnull=True))),
        name="show_building_normal"),
    url(r'^building/(?P<pk>\d+)/$', views.BuildingDetailView.as_view(),
        name="show_building"),
    url(r'^worksite/all/$', views.WorksiteListView.as_view(),
        name="show_worksite_all"),
    url(r'^worksite/participative/$',
        views.WorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=True)),
        name="show_worksite_participative"),
    url(r'^worksite/normal/$',
        views.WorksiteListView.as_view(
            queryset=models.Worksite.objects.filter(
                participative=False)),
        name="show_worksite_normal"),
    url(r'^worksite/(?P<pk>\d+)/$', views.WorksiteDetailView.as_view(),
        name="show_worksite"),
    url(r'^event/all/$', views.EventListView.as_view(),
        name="show_event_all"),
    url(r'^event/type/(?P<type>[a-zA-Z0-9_\-]+)/$',
        views.EventListView.as_view(),
        name="show_event_of_type"),
    url(r'^event/(?P<pk>\d+)/$', views.EventDetailView.as_view(),
        name="show_event"),
    url(r'^people/all/$', views.StakeholderListView.as_view(),
        name="show_stakeholder_all"),
    url(r'^people/role/(?P<role>[a-zA-Z0-9_\-]+)/$',
        views.StakeholderListView.as_view(),
        name="show_stakeholder_of_role"),
    url(r'^people/(?P<pk>\d+)/$', views.StakeholderDetailView.as_view(),
        name="show_stakeholder"),
    url(r'^building/(?P<pk>\d+)/edit/$', views.BuildingUpdateView.as_view(),
        name="edit_building"),
    url(r'^worksite/(?P<pk>\d+)/edit/$',
        views.WorksiteUpdateView.as_view(), name="edit_worksite"),
    url(r'^event/(?P<pk>\d+)/edit/$', views.EventUpdateView.as_view(),
        name="edit_event"),
    url(r'^people/(?P<pk>\d+)/edit/$', views.StakeholderUpdateView.as_view(),
        name="edit_stakeholder"),
    url(r'^building/(?P<pk>\d+)/delete/$',
        views.BuildingDeleteView.as_view(), name="delete_building"),
    url(r'^worksite/(?P<pk>\d+)/delete/$',
        views.WorksiteDeleteView.as_view(), name="delete_worksite"),
    url(r'^event/(?P<pk>\d+)/delete/$', views.EventDeleteView.as_view(),
        name="delete_event"),
    url(r'^people/(?P<pk>\d+)/delete/$', views.StakeholderDeleteView.as_view(),
        name="delete_stakeholder"),
    url(r'^building/add/$', views.BuildingCreateView.as_view(),
        name="add_building"),
    url(r'^worksite/add/$', views.WorksiteCreateView.as_view(),
        name="add_worksite"),
    url(r'^event/add/$', views.EventCreateView.as_view(),
        name="add_event"),
    url(r'^people/add/$', views.StakeholderCreateView.as_view(),
        name="add_stakeholder"),
    url(r'^building/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationBuildingView.as_view(),
        name="toggle_rec_building"),
    url(r'^worksite/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationWorksiteView.as_view(),
        name="toggle_rec_worksite"),
    url(r'^event/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationEventView.as_view(),
        name="toggle_rec_event"),
    url(r'^people/(?P<pk>\d+)/rec/$',
        views.ToggleRecommendationStakeholderView.as_view(),
        name="toggle_rec_stakeholder"),
    url(r'^all/$', views.BigMapView.as_view(),
        name="show_bigmap"),
    url(r"^profile/(?P<slug>[\w\._-]+)/$", views.ProfileDetailView.as_view(),
        name="profile_detail"),
    url(r"^profiles/all/$", views.ProfileListView.as_view(),
        name="profile_list"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/building/geojson/$',
        views.GeoJSONProfileCreatorBuildingListView.as_view(),
        name="geojson_profile_creator_building"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/worksite/geojson/$',
        views.GeoJSONProfileCreatorWorksiteListView.as_view(),
        name="geojson_profile_creator_worksite"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/event/geojson/$',
        views.GeoJSONProfileCreatorEventListView.as_view(),
        name="geojson_profile_creator_event"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/people/geojson/$',
        views.GeoJSONProfileCreatorStakeholderListView.as_view(),
        name="geojson_profile_creator_stakeholder"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/building/geojson/$',
        views.GeoJSONProfileRecommendBuildingListView.as_view(),
        name="geojson_profile_recommend_building"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/worksite/geojson/$',
        views.GeoJSONProfileRecommendWorksiteListView.as_view(),
        name="geojson_profile_recommend_worksite"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/event/geojson/$',
        views.GeoJSONProfileRecommendEventListView.as_view(),
        name="geojson_profile_recommend_event"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/people/geojson/$',
        views.GeoJSONProfileRecommendStakeholderListView.as_view(),
        name="geojson_profile_recommend_stakeholder"),
]
