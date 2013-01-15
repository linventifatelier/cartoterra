from django.conf.urls.defaults import *
from profiles import views

urlpatterns = patterns("",
    url(r"^profile/(?P<slug>[\w\._-]+)/$", views.ProfileDetail.as_view(), name="profile_detail"),
    #url(r'^patrimony/(?P<pk>\d+)/$', views.PatrimonyDetail.as_view(),
)
