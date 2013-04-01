from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from geodata.views import BigMapView

from haystack.forms import ModelSearchForm
from haystack.views import SearchView, search_view_factory

import haystack
haystack.autodiscover()


from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()


urlpatterns = patterns(
    "",
    url(r'^$', BigMapView.as_view(), name="home"),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #url(r'^my_admin/jsi18n',
    #    include('django.views.i18n.null_javascript_catalog')),
    url(r"^geodata/", include("geodata.urls")),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^profiles/", include("profiles.urls")),
    url(r"^account/", include("account.urls")),
    url(r'^knowledge/', include('knowledge.urls')),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^search/', include('haystack.urls')),
    url(r'^searchbis/',
        search_view_factory(view_class=SearchView, form_class=ModelSearchForm),
        name="searchbis"),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
                                url(r'^rosetta/',
                                    include('rosetta.urls')),
                                )
