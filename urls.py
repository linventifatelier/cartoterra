from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from pinax.apps.account.openid_consumer import PinaxConsumer

from django.contrib.gis import admin
admin.autodiscover()

from geodata.views import  *


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r'^kml/all.kml$', all_kml),
    url(r'^kml/patrimony.kml$', patrimony_kml),
    url(r'^kml/meeting.kml$', meeting_kml),
    url(r'^kml/construction.kml$', construction_kml),
    url(r'^construction/(?P<id>[0-9] *)/', construction_page),
    url(r'^map/', map_page),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
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
    )
