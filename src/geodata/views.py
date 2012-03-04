"""GeoData views."""

from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from models import EarthGeoDataPatrimony, EarthGeoDataConstruction,\
     EarthGeoDataMeeting
from forms import EarthGeoDataPatrimonyForm
from olwidget.widgets import InfoMap, Map, InfoLayer
from sorl.thumbnail import get_thumbnail


def _info_builder(geodata):
    info = []
    for i in geodata.objects.all():
        description = ""
        image = ""

        if i.description:
            description = i.description
        else: description = i.name

        if i.image:
            thumbnail = get_thumbnail(i.image, '100x100')
            image = "<p><a href=/" + i.classurl + "/" + str(i.id) +\
                    "/><img src=\"" + thumbnail.url + "\" width=\"" +\
                    str(thumbnail.x) + "\" height=\"" + str(thumbnail.y) +\
                    "\"></a></p>"


        info.append([i.geometry,
                     "<h1>" + i.name + "</h1>" +\
                     "<p><a href=/" + i.classurl + "/" + str(i.id) + "/>" +\
                     description + "</a></p>" + image
                     ])
    return info


def show_patrimony_all(_):
    """Returns a template to present all patrimonies."""
    geodata = EarthGeoDataPatrimony.objects.all()
    map_ = InfoMap(_info_builder(EarthGeoDataPatrimony),
                   {'name': "Patrimonies",
                    'overlay_style': {'fill_color': 'red',}})
    return direct_to_template(_, 'show_patrimony_all.html',
                              {'geodata': geodata, 'map': map_})


def show_construction_all(_):
    """Returns a template to present all constructions."""
    geodata = EarthGeoDataConstruction.objects.all()
    map_ = InfoMap(_info_builder(EarthGeoDataConstruction),
                   {'name': "Constructions",
                    'overlay_style': {'fill_color': 'blue',}})
    return direct_to_template(_, 'show_construction_all.html',
                              {'geodata': geodata, 'map': map_})


def show_meeting_all(_):
    """Returns a template to present all meetings."""
    geodata = EarthGeoDataMeeting.objects.all()
    map_ = InfoMap(_info_builder(EarthGeoDataMeeting),
                   {'name': "Meetings",
                    'overlay_style': {'fill_color': 'green',}})
    return direct_to_template(_, 'show_meeting_all.html',
                              {'geodata': geodata, 'map': map_})


def show_bigmap(request):
    """Returns a big Map with all geodatas."""
    lcount_patrimony = EarthGeoDataPatrimony.objects.all().count()
    lcount_construction = EarthGeoDataConstruction.objects.all().count()
    lcount_meeting = EarthGeoDataMeeting.objects.all().count()
    lcount = lcount_patrimony + lcount_construction + lcount_meeting

    map_ = Map([
       InfoLayer(_info_builder(EarthGeoDataPatrimony),
                 {'name': "Patrimonies",
                  'overlay_style': {'fill_color': 'red',}}),
       InfoLayer(_info_builder(EarthGeoDataConstruction),
                 {'name': "Constructions",
                  'overlay_style': {'fill_color': 'blue',}}),
       InfoLayer(_info_builder(EarthGeoDataMeeting),
                 {'name': "Meetings",
                  'overlay_style': {'fill_color': 'green',}}),
    ], {'map_div_class': 'bigmap'})
    return direct_to_template(request, 'show_bigmap.html',
                              { 'map': map_, 'location_count': lcount,
                                'patrimony_count': lcount_patrimony,
                                'construction_count': lcount_construction,
                                'meeting_count': lcount_meeting,})


def show_patrimony(request, ident):
    """Returns patrimony.html template."""
    geodata = get_object_or_404(EarthGeoDataPatrimony, pk=ident)
    map_ = InfoMap([[geodata.geometry, ""]],
                   {'fill_color': 'red'})
    return direct_to_template(request, 'show_patrimony.html',
                              {'map': map_, 'place': geodata})


def show_construction(request, ident):
    """Returns construction.html template."""
    geodata = get_object_or_404(EarthGeoDataConstruction, pk=ident)
    map_ = InfoMap([[geodata.geometry, ""]],
                   {'fill_color': 'red'})
    return direct_to_template(request, 'show_construction.map',
                              {'html': map_, 'place': geodata})


def show_meeting(request, ident):
    """Returns meeting.html template."""
    geodata = get_object_or_404(EarthGeoDataMeeting, pk=ident)
    map_ = InfoMap([[geodata.geometry, ""]],
                   {'fill_color': 'red'})
    return direct_to_template(request, 'show_meeting.html',
                              {'map': map_, 'place': geodata})


def add_patrimony(request):
    if request.method == "POST":
        form = EarthGeoDataPatrimonyForm(request.POST)
    else:
        form = EarthGeoDataPatrimonyForm() # An unbound form

    return direct_to_template(request, 'add_patrimony.html', {
        'form': form,
        })
