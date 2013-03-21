from django.conf.urls import *
from profiles.views import *
from geodata import views as geodataviews
from geodata.models import *

urlpatterns = patterns("",
    url(r"^profile/(?P<slug>[\w\._-]+)/$", ProfileDetailView.as_view(), name="profile_detail"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/patrimony/geojson/$',
        GeoJSONProfileCreatorPatrimonyListView.as_view(),
        name="geojson_profile_creator_patrimony"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/construction/geojson/$',
        GeoJSONProfileCreatorConstructionListView.as_view(),
        name="geojson_profile_creator_construction"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/meeting/geojson/$',
        GeoJSONProfileCreatorMeetingListView.as_view(),
        name="geojson_profile_creator_meeting"),
    url(r'^profile/(?P<slug>[\w\._-]+)/creator/actor/geojson/$',
        GeoJSONProfileCreatorActorListView.as_view(),
        name="geojson_profile_creator_actor"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/patrimony/geojson/$',
        GeoJSONProfileRecommendPatrimonyListView.as_view(),
        name="geojson_profile_recommend_patrimony"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/construction/geojson/$',
        GeoJSONProfileRecommendConstructionListView.as_view(),
        name="geojson_profile_recommend_construction"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/meeting/geojson/$',
        GeoJSONProfileRecommendMeetingListView.as_view(),
        name="geojson_profile_recommend_meeting"),
    url(r'^profile/(?P<slug>[\w\._-]+)/recommend/actor/geojson/$',
        GeoJSONProfileRecommendActorListView.as_view(),
        name="geojson_profile_recommend_actor"),
)
