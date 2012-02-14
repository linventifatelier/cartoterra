"""urls file."""
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from pinax.apps.account.openid_consumer import PinaxConsumer

from django.contrib.gis import admin
admin.autodiscover()

from geodata.views import *
import os


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r'^kml/patrimonies.kml$', patrimony_kml),
    url(r'^kml/meetings.kml$', meeting_kml),
    url(r'^kml/constructions.kml$', construction_kml),
    url(r'^patrimonies.html$', patrimonies_all),
    url(r'^meetings.html$', meetings_all),
    url(r'^constructions.html$', constructions_all),
    url(r'^construction/(?P<ident>[0-9] *)/', construction_page),
    url(r'^patrimony/(?P<ident>[0-9] *)/', patrimony_page),
    url(r'^meeting/(?P<ident>[0-9] *)/', meeting_page),
    url(r'^map/', map_page),
    url(r'^i18n/', include('django.conf.urls.i18n')),
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
