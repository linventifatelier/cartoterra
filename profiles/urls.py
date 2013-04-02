from django.conf.urls import patterns, url
from profiles.views import ProfileDetailView, ProfileListView, \
    GeoJSONProfileCreatorBuildingListView, \
    GeoJSONProfileCreatorWorksiteListView, \
    GeoJSONProfileCreatorEventListView, \
    GeoJSONProfileCreatorStakeholderListView, \
    GeoJSONProfileRecommendBuildingListView, \
    GeoJSONProfileRecommendWorksiteListView, \
    GeoJSONProfileRecommendEventListView, \
    GeoJSONProfileRecommendStakeholderListView


urlpatterns = patterns(
    "",
    url(r"^profile/(?P<slug>[\w\._-]+)/$", ProfileDetailView.as_view(),
        name="profile_detail"),
    url(r"^all/$", ProfileListView.as_view(), name="profile_list"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/patrimony/geojson/$',
        GeoJSONProfileCreatorBuildingListView.as_view(),
        name="geojson_profile_creator_patrimony"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/construction/geojson/$',
        GeoJSONProfileCreatorWorksiteListView.as_view(),
        name="geojson_profile_creator_construction"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/meeting/geojson/$',
        GeoJSONProfileCreatorEventListView.as_view(),
        name="geojson_profile_creator_meeting"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/actor/geojson/$',
        GeoJSONProfileCreatorStakeholderListView.as_view(),
        name="geojson_profile_creator_actor"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/patrimony/geojson/$',
        GeoJSONProfileRecommendBuildingListView.as_view(),
        name="geojson_profile_recommend_patrimony"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/construction/geojson/$',
        GeoJSONProfileRecommendWorksiteListView.as_view(),
        name="geojson_profile_recommend_construction"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/meeting/geojson/$',
        GeoJSONProfileRecommendEventListView.as_view(),
        name="geojson_profile_recommend_meeting"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/actor/geojson/$',
        GeoJSONProfileRecommendStakeholderListView.as_view(),
        name="geojson_profile_recommend_actor"),
)
