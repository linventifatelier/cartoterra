"""urls file."""
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from pinax.apps.account.openid_consumer import PinaxConsumer

from django.contrib.gis import admin
admin.autodiscover()

from geodata.views import *
import os

from haystack.forms import ModelSearchForm
from haystack.views import SearchView, search_view_factory

import haystack
haystack.autodiscover()

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    #url(r"^$", direct_to_template, {
    #    "template": "homepage.html",
    #}, name="home"),
    url(r'^$', show_bigmap, name="home"),
    url(r'^all/patrimony/$', show_patrimony_all),
    url(r'^all/construction/$', show_construction_all),
    url(r'^all/meeting/$', show_meeting_all),
    url(r'^patrimony/(?P<ident>\d+)/', show_patrimony),
    url(r'^construction/(?P<ident>\d+)/', show_construction),
    url(r'^meeting/(?P<ident>\d+)/', show_meeting),
    url(r'^edit/patrimony/(?P<ident>\d+)/$', edit_patrimony),
    url(r'^edit/construction/(?P<ident>\d+)/$', edit_construction),
    url(r'^edit/meeting/(?P<ident>\d+)/$', edit_meeting),
    url(r'^delete/patrimony/(?P<ident>\d+)/$', delete_patrimony),
    url(r'^add/patrimony/$', add_patrimony),
    url(r'^add/construction/$', add_construction),
    url(r'^add/meeting/$', add_meeting),
    url(r'^user/(?P<userid>\d+)/', show_usermap),
    url(r'^map/', show_bigmap),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #url(r'^my_admin/jsi18n', include('django.views.i18n.null_javascript_catalog')),

    url(r"^admin/invite_user/$",
        "pinax.apps.signup_codes.views.admin_invite_user",
        name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^search/', include('haystack.urls')),
    url(r'^searchbis/', search_view_factory(
                           view_class=SearchView,
                           form_class=ModelSearchForm,
    ), name="searchbis"),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
                            url(r"", include("staticfiles.urls")),
                            url(r'^site_media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root':
                                 os.path.join(os.path.dirname(__file__),
                                              "site_media")}),
                            )
