"""GeoData views."""
# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.contrib.gis.shortcuts import render_to_kml
from models import InterestingLocation, EarthGeoDataMeeting, \
     EarthGeoDataPatrimony, EarthGeoDataConstruction


def patrimony_kml(_):
    """Returns a kml file of all patrimony locations."""
    locations = EarthGeoDataPatrimony.objects.kml()
    return render_to_kml("patrimonies.kml", {'places': locations, 'type_url': 'patrimony'})


def meeting_kml(_):
    """Returns a kml file of all meeting locations."""
    locations = EarthGeoDataMeeting.objects.kml()
    return render_to_kml("meetings.kml", {'places': locations, 'type_url': 'meeting'})


def construction_kml(_):
    """Returns a kml file of all construction locations."""
    locations = EarthGeoDataConstruction.objects.kml()
    return render_to_kml("constructions.kml", {'places': locations, 'type_url': 'construction'})


def map_page(request):
    """Returns map.html template."""
    lcount = InterestingLocation.objects.all().count()
    return direct_to_template(request, 'map.html', {'location_count': lcount})


def construction_page(request, ident):
    """Returns construction.html template."""
    construction = get_object_or_404(EarthGeoDataConstruction, pk=ident)
    return direct_to_template(request, 'construction.html',
                              {'place': construction})

def patrimony_page(request, ident):
    """Returns patrimony.html template."""
    patrimony = get_object_or_404(EarthGeoDataPatrimony, pk=ident)
    return direct_to_template(request, 'patrimony.html',
                              {'place': patrimony})

def meeting_page(request, ident):
    """Returns meeting.html template."""
    meeting = get_object_or_404(EarthGeoDataMeeting, pk=ident)
    return direct_to_template(request, 'meeting.html',
                              {'place': meeting})
