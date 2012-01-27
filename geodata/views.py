# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.contrib.gis.shortcuts import render_to_kml
from geodata.models import  *
 

def all_kml(request):
    locations  = InterestingLocation.objects.kml()
    return render_to_kml("placemarks.kml", {'places' : locations}) 

def patrimony_kml(request):
    locations  = EarthGeoDataPatrimony.objects.kml()
    return render_to_kml("placemarks.kml", {'places' : locations}) 

def meeting_kml(request):
    locations  = EarthGeoDataMeeting.objects.kml()
    return render_to_kml("placemarks.kml", {'places' : locations}) 

def construction_kml(request):
    locations  = EarthGeoDataConstruction.objects.kml()
    return render_to_kml("placemarks.kml", {'places' : locations}) 

def map_page(request):
    lcount = InterestingLocation.objects.all().count()
    return direct_to_template(request,'map.html', {'location_count' : lcount})

def construction_page(request,id):
    construction = get_object_or_404(EarthGeoDataConstruction, pk=id)
    return direct_to_template(request,'construction.html', {'construction' : construction})
