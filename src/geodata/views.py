"""GeoData views."""

from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from models import EarthGeoDataPatrimony, EarthGeoDataConstruction,\
     EarthGeoDataMeeting
from forms import EarthGeoDataPatrimonyForm, EarthGeoDataConstructionForm,\
     EarthGeoDataMeetingForm
from olwidget.widgets import InfoMap, Map, InfoLayer
from sorl.thumbnail import get_thumbnail
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import list_detail, create_update
from django.contrib.auth.models import User




def _info_builder(geodataobjects):
    info = []
    for i in geodataobjects:
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
    map_ = InfoMap(_info_builder(geodata),
                   {'name': "Patrimonies",
                    'overlay_style': {'fill_color': 'red',}})
    return direct_to_template(_, 'show_patrimony_all.html',
                              {'geodata': geodata,
                               'classurl': 'patrimony',
                               'classname': 'Patrimony',
                               'map': map_ })


def show_construction_all(_):
    """Returns a template to present all constructions."""
    geodata = EarthGeoDataConstruction.objects.all()
    map_ = InfoMap(_info_builder(geodata),
                   {'name': "Constructions",
                    'overlay_style': {'fill_color': 'blue',}})
    return direct_to_template(_, 'show_construction_all.html',
                              {'geodata': geodata,
                               'classurl': 'construction',
                               'classname': 'Construction',
                               'map': map_})


def show_meeting_all(_):
    """Returns a template to present all meetings."""
    geodata = EarthGeoDataMeeting.objects.all()
    map_ = InfoMap(_info_builder(geodata),
                   {'name': "Meetings",
                    'overlay_style': {'fill_color': 'green',}})
    return direct_to_template(_, 'show_meeting_all.html',
                              {'geodata': geodata,
                               'classurl': 'meeting',
                               'classname': 'Meeting',
                               'map': map_})


def show_bigmap(request):
    """Returns a big Map with all geodatas."""
    patrimony = EarthGeoDataPatrimony.objects.all()
    construction = EarthGeoDataConstruction.objects.all()
    meeting = EarthGeoDataMeeting.objects.all()
    lcount_patrimony = patrimony.count()
    lcount_construction = construction.count()
    lcount_meeting = meeting.count()
    lcount = lcount_patrimony + lcount_construction + lcount_meeting

    map_ = Map([
       InfoLayer(_info_builder(patrimony),
                 {'name': "Patrimonies",
                  'overlay_style': {'fill_color': 'red',}}),
       InfoLayer(_info_builder(construction),
                 {'name': "Constructions",
                  'overlay_style': {'fill_color': 'blue',}}),
       InfoLayer(_info_builder(meeting),
                 {'name': "Meetings",
                  'overlay_style': {'fill_color': 'green',}}),
    ], {'map_div_class': 'bigmap'})
    return direct_to_template(request, 'show_bigmap.html',
                              { 'map': map_, 'location_count': lcount,
                                'patrimony_count': lcount_patrimony,
                                'construction_count': lcount_construction,
                                'meeting_count': lcount_meeting,})


def show_usermap(request, userid):
    """Returns a show_usermap.html template."""
    user_ = get_object_or_404(User, pk=userid)
    patrimony = EarthGeoDataPatrimony.objects.filter(creator = user_)
    construction = EarthGeoDataConstruction.objects.filter(creator = user_)
    meeting = EarthGeoDataMeeting.objects.filter(creator = user_)
    lcount_patrimony = patrimony.count()
    lcount_construction = construction.count()
    lcount_meeting = meeting.count()
    lcount = lcount_patrimony + lcount_construction + lcount_meeting

    map_ = Map([
       InfoLayer(_info_builder(patrimony),
                 {'name': "Patrimonies " + user_.username,
                  'overlay_style': {'fill_color': 'red',}}),
       InfoLayer(_info_builder(construction),
                 {'name': "Constructions " + user_.username,
                  'overlay_style': {'fill_color': 'blue',}}),
       InfoLayer(_info_builder(meeting),
                 {'name': "Meetings " + user_.username,
                  'overlay_style': {'fill_color': 'green',}}),
    ], {'map_div_class': 'usermap'})
    return direct_to_template(request, 'show_usermap.html',
                              { 'map': map_,
                                'user_': user_,
                                'location_count': lcount,
                                'patrimony_count': lcount_patrimony,
                                'construction_count': lcount_construction,
                                'meeting_count': lcount_meeting,})


def show_patrimony(request, ident):
    """Returns show_patrimony.html template."""
    geodata = get_object_or_404(EarthGeoDataPatrimony, pk=ident)
    map_ = InfoMap([[geodata.geometry, ""]],
                   {'fill_color': 'red'})
    return direct_to_template(request, 'show_patrimony.html',
                              {'map': map_, 'geodata': geodata})


def show_construction(request, ident):
    """Returns show_construction.html template."""
    geodata = get_object_or_404(EarthGeoDataConstruction, pk=ident)
    map_ = InfoMap([[geodata.geometry, ""]],
                   {'fill_color': 'red'})
    return direct_to_template(request, 'show_construction.html',
                              {'map': map_, 'geodata': geodata})


def show_meeting(request, ident):
    """Returns show_meeting.html template."""
    geodata = get_object_or_404(EarthGeoDataMeeting, pk=ident)
    map_ = InfoMap([[geodata.geometry, ""]],
                   {'fill_color': 'red'})
    return direct_to_template(request, 'show_meeting.html',
                              {'map': map_, 'geodata': geodata})



error_message = _("Please correct the errors below.")


@login_required
def _add_builder(request, geodatamodel, geodatamodelform, geodatatemplate):
    geodata = geodatamodel(creator = request.user,
                           pub_date = datetime.now())

    if request.method == "POST":
        form = geodatamodelform(request.POST, instance = geodata)
        if form.is_valid():
            obj = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully added %(classurl)s \"%(name)s\".") %
                                 {"classurl": obj.classurl, "name": obj.name,}
                                 )
            return HttpResponseRedirect('/%(classurl)s/%(ident)d/' %
                                        { 'classurl': obj.classurl, 'ident': obj.id })
        else:
            messages.add_message(request, messages.ERROR,
                                 error_message
                                 )
    else:
        form = geodatamodelform(instance = geodata) # An unbound form

    return direct_to_template(request, geodatatemplate, {
        'form': form,
        })


@login_required
def add_patrimony(request):
    return _add_builder(request, EarthGeoDataPatrimony, EarthGeoDataPatrimonyForm, 'add_patrimony.html')


@login_required
def add_construction(request):
    return _add_builder(request, EarthGeoDataConstruction, EarthGeoDataConstructionForm, 'add_construction.html')


@login_required
def add_meeting(request):
    return _add_builder(request, EarthGeoDataMeeting, EarthGeoDataMeetingForm, 'add_meeting.html')



@login_required
def _edit_builder(request, geodatamodel, geodatamodelform, geodatatemplate, ident):
    geodata = get_object_or_404(geodatamodel, pk=ident)
    if geodata.creator != request.user:
        raise HttpResponseForbidden()

    if request.method == "POST":
        form = geodatamodelform(request.POST, instance = geodata)
        if form.is_valid():
            obj = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully edited %(classurl)s \"%(name)s\".") %
                                 { 'classurl': obj.classurl, "name": obj.name, }
                                 )
            return HttpResponseRedirect('/%(classurl)s/%(ident)d/' %
                                        { 'classurl': obj.classurl,
                                          'ident': obj.id })
        else:
            messages.add_message(request, messages.ERROR,
                                 error_message
                                 )
    else:
        form = geodatamodelform(instance = geodata) # An unbound form

    return direct_to_template(request, geodatatemplate, {
        'form': form,
        'geodata': geodata,
        })


@login_required
def edit_patrimony(request, ident):
    return _edit_builder(request, EarthGeoDataPatrimony,
                         EarthGeoDataPatrimonyForm, 'edit_patrimony.html', ident)



@login_required
def edit_construction(request, ident):
    return _edit_builder(request, EarthGeoDataConstruction,
                         EarthGeoDataConstructionForm, 'edit_construction.html', ident)


@login_required
def edit_meeting(request, ident):
    return _edit_builder(request, EarthGeoDataMeeting,
                         EarthGeoDataMeetingForm, 'edit_meeting.html', ident)




@login_required
def _delete_builder(request, geodatamodel, geodatatemplate, ident):
    geodata = get_object_or_404(geodatamodel, pk=ident)

    if geodata.creator != request.user:
        raise HttpResponseForbidden()

    if request.method == 'POST':
        geodata.delete()
        messages.add_message(request, messages.SUCCESS,
                             _("Successfully deleted %(classurl)s \"%(name)s\".") %
                             { 'classurl': geodata.classurl, "name": geodata.name, }
                             )
        return HttpResponseRedirect('/')
    else:
        return direct_to_template(request, geodatatemplate, {
            'geodata': geodata,
        })


@login_required
def delete_patrimony(request, ident):
    return _delete_builder(request, EarthGeoDataPatrimony, 'delete_patrimony.html', ident)


@login_required
def delete_construction(request, ident):
    return _delete_builder(request, EarthGeoDataConstruction, 'delete_construction.html', ident)


@login_required
def delete_meeting(request, ident):
    return _delete_builder(request, EarthGeoDataMeeting, 'delete_meeting.html', ident)
