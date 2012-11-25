from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from geodata.views import *
import os

from haystack.forms import ModelSearchForm
from haystack.views import SearchView, search_view_factory

from profiles.views import *


import haystack
haystack.autodiscover()

urlpatterns = patterns("",
    url(r'^$', show_bigmap, name="home"),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #url(r'^my_admin/jsi18n', include('django.views.i18n.null_javascript_catalog')),
    url(r"^geodata/", include("geodata.urls")),
    url(r"^admin/", include(admin.site.urls)),

    url(r"^account/", include("account.urls")),
    #url(r"^profiles/profile/(?P<username>[\w\._-]+)/$",
    #    ProfileDetailView.as_view(), name="profile_detail"),
    #url(r"^profiles/(?P<profile_slug>[\w\._-]+)/profile/(?P<profile_pk>\d+)/$",
    #    ProfileDetailView.as_view(), name="profile_detail"),
    #url(r"^profiles/", include("idios.urls")),
    url(r"^profiles/", include("userena.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^search/', include('haystack.urls')),
    url(r'^searchbis/', search_view_factory(
                           view_class=SearchView,
                           form_class=ModelSearchForm,
    ), name="searchbis"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
                                url(r'^rosetta/',
                                    include('rosetta.urls')),
                                )

