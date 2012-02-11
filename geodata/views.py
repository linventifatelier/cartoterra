"""GeoData views."""

from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.contrib.gis.shortcuts import render_to_kml

from models import EarthGeoDataMeeting, EarthGeoDataPatrimony, \
     EarthGeoDataConstruction


def patrimony_kml(_):
    """Returns a kml file of all patrimony locations."""
    locations = EarthGeoDataPatrimony.objects.kml()
    return render_to_kml("patrimonies.kml", {'places': locations, 'type_url':
    'patrimony'})


def meeting_kml(_):
    """Returns a kml file of all meeting locations."""
    locations = EarthGeoDataMeeting.objects.kml()
    return render_to_kml("meetings.kml", {'places': locations, 'type_url':
    'meeting'})


def construction_kml(_):
    """Returns a kml file of all construction locations."""
    locations = EarthGeoDataConstruction.objects.kml()
    return render_to_kml("constructions.kml", {'places': locations, 'type_url':
    'construction'})


def map_page(request):
    """Returns map.html template."""
    lcount_construction = EarthGeoDataConstruction.objects.all().count()
    lcount_patrimony = EarthGeoDataPatrimony.objects.all().count()
    lcount_meeting = EarthGeoDataMeeting.objects.all().count()
    lcount = lcount_meeting + lcount_patrimony + lcount_construction
    return direct_to_template(request, 'map.html', {'location_count': lcount,
    'construction_count': lcount_construction, 'meeting_count': lcount_meeting,
    'patrimony_count': lcount_patrimony, })


def construction_page(request, ident):
    """Returns construction.html template."""
    construction = get_object_or_404(EarthGeoDataConstruction, pk=ident)
    return direct_to_template(request, 'construction.html', {'place':
    construction})


def patrimony_page(request, ident):
    """Returns patrimony.html template."""
    patrimony = get_object_or_404(EarthGeoDataPatrimony, pk=ident)
    return direct_to_template(request, 'patrimony.html', {'place': patrimony})


def meeting_page(request, ident):
    """Returns meeting.html template."""
    meeting = get_object_or_404(EarthGeoDataMeeting, pk=ident)
    return direct_to_template(request, 'meeting.html', {'place': meeting})
