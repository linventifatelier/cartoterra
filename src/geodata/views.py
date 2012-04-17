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
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import list_detail, create_update
from django.contrib.auth.models import User
from profiles.models import Profile
from django.conf import settings
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser







def _info_builder(geodataobjects, style = {}):
    info = []

    for i in geodataobjects:
        description = ""
        image = ""

        if i.description:
            description = i.description
        else: description = i.name

        if i.image:
            thumbnail = get_thumbnail(i.image, '100x100')
            image = "<p><a href=" + i.get_absolute_url() +\
                    "><img src=\"" + thumbnail.url + "\" width=\"" +\
                    str(thumbnail.x) + "\" height=\"" + str(thumbnail.y) +\
                    "\"></a></p>"

        mydict = { 'html': "<h1>" + i.name + "</h1>" +\
                       "<p><a href=" + i.get_absolute_url() + ">" +\
                       description + "</a></p>" + image,
                   'style': style
                   }

        info.append([ i.geometry, mydict ])
    return info


def show_patrimony_all(_):
    """Returns a template to present all patrimonies."""
    geodata_list = EarthGeoDataPatrimony.objects.all()
    map_ = InfoMap(_info_builder(geodata_list),
                   {'name': "Patrimonies",
                    'overlay_style': {
                        'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                        'graphic_width': 20,
                        'graphic_height': 20,
                        'fill_color': '#00FF00',
                        'stroke_color': '#008800',
                        },
                    'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                    })
    return direct_to_template(_, 'show_patrimony_all.html',
                              {'geodata_list': geodata_list,
                               'map': map_ })


def show_construction_all(_):
    """Returns a template to present all constructions."""
    geodata_list = EarthGeoDataConstruction.objects.all()
    map_ = InfoMap(_info_builder(geodata_list),
                   {'name': "Constructions",
                    'overlay_style': {
                        'external_graphic': settings.STATIC_URL+"img/construction.png",
                        'graphic_width': 20,
                        'graphic_height': 20,
                        'fill_color': '#00FF00',
                        'stroke_color': '#008800',
                        },
                    'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                    })
    return direct_to_template(_, 'show_construction_all.html',
                              {'geodata_list': geodata_list,
                               'map': map_})


def show_meeting_all(_):
    """Returns a template to present all meetings."""
    geodata_list = EarthGeoDataMeeting.objects.all()
    map_ = InfoMap(_info_builder(geodata_list),
                   {'name': "Meetings",
                    'overlay_style': {
                        'external_graphic': settings.STATIC_URL+"img/meeting.png",
                        'graphic_width': 20,
                        'graphic_height': 20,
                        'fill_color': '#00FF00',
                        'stroke_color': '#008800',
                        },
                    'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }
                    })
    return direct_to_template(_, 'show_meeting_all.html',
                              {'geodata_list': geodata_list,
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
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(construction),
                 {'name': "Constructions",
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/construction.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(meeting),
                 {'name': "Meetings",
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/meeting.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
    ], {'map_div_class': 'bigmap'})
    return direct_to_template(request, 'show_bigmap.html',
                              { 'map': map_, 'location_count': lcount,
                                'patrimony_count': lcount_patrimony,
                                'construction_count': lcount_construction,
                                'meeting_count': lcount_meeting,})

def get_profilemap(profile):
    user_ = profile.user
    patrimony = EarthGeoDataPatrimony.objects.filter(creator = user_)
    construction = EarthGeoDataConstruction.objects.filter(creator = user_)
    meeting = EarthGeoDataMeeting.objects.filter(creator = user_)
    r_patrimony = profile.r_patrimony.all()
    r_construction = profile.r_construction.all()
    r_meeting = profile.r_meeting.all()
    name = user_.username

    map_ = Map([
       InfoLayer(_info_builder(patrimony),
                 {'name': "Patrimonies " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(construction),
                 {'name': "Constructions " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/construction.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(meeting),
                 {'name': "Meetings " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/meeting.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_patrimony, {
                            'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                            'graphic_width': 10,
                            'graphic_height': 10,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            }) +
                 _info_builder(r_construction, {
                            'external_graphic': settings.STATIC_URL+"img/construction.png",
                            'graphic_width': 10,
                            'graphic_height': 10,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            }) +
                 _info_builder(r_meeting, {
                            'external_graphic': settings.STATIC_URL+"img/meeting.png",
                            'graphic_width': 10,
                            'graphic_height': 10,
                            'fill_color': '#00FF00',
                            'stroke_color': '#008800',
                            }) ,
                 {'name': "Recommendations " + name, }),
    ], {'map_div_class': 'usermap'})
    return map_

def show_usermap(request, userid):
    """Returns a show_usermap.html template."""
    profile = get_object_or_404(Profile, pk=userid)
    user_ = profile.user
    patrimony = EarthGeoDataPatrimony.objects.filter(creator = user_)
    construction = EarthGeoDataConstruction.objects.filter(creator = user_)
    meeting = EarthGeoDataMeeting.objects.filter(creator = user_)
    r_patrimony = profile.r_patrimony.all()
    r_construction = profile.r_construction.all()
    r_meeting = profile.r_meeting.all()
    lcount_patrimony = patrimony.count()
    lcount_construction = construction.count()
    lcount_meeting = meeting.count()
    lcount = lcount_patrimony + lcount_construction + lcount_meeting
    lcount_r_patrimony = r_patrimony.count()
    lcount_r_construction = r_construction.count()
    lcount_r_meeting = r_meeting.count()
    lcount_r = lcount_r_patrimony + lcount_r_construction + lcount_r_meeting
    name = user_.username

    map_ = Map([
       InfoLayer(_info_builder(patrimony),
                 {'name': "Patrimonies " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(construction),
                 {'name': "Constructions " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/construction.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(meeting),
                 {'name': "Meetings " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/meeting.png",
                      'graphic_width': 20,
                      'graphic_height': 20,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_patrimony),
                 {'name': "Recommendations: Patrimonies " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                      'graphic_width': 10,
                      'graphic_height': 10,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_construction),
                 {'name': "Recommendations: Constructions " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/construction.png",
                      'graphic_width': 10,
                      'graphic_height': 10,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
       InfoLayer(_info_builder(r_meeting),
                 {'name': "Recommendations: Meetings " + name,
                  'overlay_style': {
                      'external_graphic': settings.STATIC_URL+"img/meeting.png",
                      'graphic_width': 10,
                      'graphic_height': 10,
                      'fill_color': '#00FF00',
                      'stroke_color': '#008800',
                      }}),
    ], {'map_div_class': 'usermap'})
    return direct_to_template(request, 'show_usermap.html',
                              { 'map': map_,
                                'user_': user_,
                                'location_count': lcount,
                                'patrimony_count': lcount_patrimony,
                                'construction_count': lcount_construction,
                                'meeting_count': lcount_meeting,
                                'r_location_count': lcount_r,
                                'r_patrimony_count': lcount_r_patrimony,
                                'r_construction_count': lcount_r_construction,
                                'r_meeting_count': lcount_r_meeting,
                                })


def _get_dict_show(request, map_, geodata, edit_func, delete_func,
                   toggle_rec_func, ident):
    user = request.user
    if isinstance(user, AnonymousUser):
        return {'map': map_, 'geodata': geodata, }
    else:
        if geodata.creator != request.user:
            profile = request.user.get_profile()
            recommendations = []
            if toggle_rec_func == 'toggle_rec_patrimony':
                recommendations = profile.r_patrimony
            elif toggle_rec_func == 'toggle_rec_construction':
                recommendations = profile.r_construction
            elif toggle_rec_func == 'toggle_rec_meeting':
                recommendations = profile.r_meeting
                if geodata in recommendations.all():
                    return {'map': map_, 'geodata': geodata,
                            'rec_off_geodata': reverse(toggle_rec_func, args=[ident]), }
                else:
                    return {'map': map_, 'geodata': geodata,
                            'rec_on_geodata': reverse(toggle_rec_func, args=[ident]), }
        else:
            return {'map': map_, 'geodata': geodata,
                    'edit_geodata': reverse(edit_func, args=[ident]),
                    'delete_geodata': reverse(delete_func, args=[ident]),}


def show_patrimony(request, ident):
    """Returns show_patrimony.html template."""
    geodata = get_object_or_404(EarthGeoDataPatrimony, pk=ident)
    map_ = InfoMap([[geodata.geometry,
                     { 'style': {
                         'external_graphic': settings.STATIC_URL+"img/patrimony.png",
                         'graphic_width': 30,
                         'graphic_height': 30,
                         'fill_color': '#00FF00',
                         'stroke_color': '#008800',
                         }}]],
                   { 'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }}
                   )
    return direct_to_template(request, 'show_patrimony.html',
                              _get_dict_show(request, map_, geodata,
                                             'edit_patrimony',
                                             'delete_patrimony',
                                             'toggle_rec_patrimony', ident,))


def show_construction(request, ident):
    """Returns show_construction.html template."""
    geodata = get_object_or_404(EarthGeoDataConstruction, pk=ident)
    map_ = InfoMap([[geodata.geometry,
                     { 'style': {
                         'external_graphic': settings.STATIC_URL+"img/construction.png",
                         'graphic_width': 30,
                         'graphic_height': 30,
                         'fill_color': '#00FF00',
                         'stroke_color': '#008800',
                         }}]],
                   { 'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }}
                   )
    return direct_to_template(request, 'show_construction.html',
                              _get_dict_show(request, map_, geodata,
                                             'edit_construction',
                                             'delete_construction',
                                             'toggle_rec_construction', ident))


def show_meeting(request, ident):
    """Returns show_meeting.html template."""
    geodata = get_object_or_404(EarthGeoDataMeeting, pk=ident)
    map_ = InfoMap([[geodata.geometry,
                     { 'style': {
                         'external_graphic': settings.STATIC_URL+"img/meeting.png",
                         'graphic_width': 30,
                         'graphic_height': 30,
                         'fill_color': '#00FF00',
                         'stroke_color': '#008800',
                         }}]],
                   { 'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] }}
                   )
    return direct_to_template(request, 'show_meeting.html',
                              _get_dict_show(request, map_, geodata,
                                             'edit_meeting',
                                             'delete_meeting',
                                             'toggle_rec_meeting', ident))



error_message = _("Please correct the errors below.")


@login_required
def _add_builder(request, geodatamodel, geodatamodelform, geodatatemplate):
    geodata = geodatamodel(creator = request.user,
                           pub_date = datetime.now())

    if request.method == "POST":
        form = geodatamodelform(request.POST, request.FILES, instance = geodata)
        if form.is_valid():
            obj = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully added %(modelname)s \"%(name)s\".") %
                                 {'modelname': force_unicode(obj._meta.verbose_name), 'name': obj.name,}
                                 )
            return HttpResponseRedirect('%s' % obj.get_absolute_url())
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
        messages.add_message(request, messages.ERROR,
                             _("You cannot edit %(modelname)s \"%(name)s\"") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
        return HttpResponseForbidden()

    if request.method == "POST":
        form = geodatamodelform(request.POST, request.FILES, instance = geodata)
        if form.is_valid():
            obj = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully edited %(modelname)s \"%(name)s\".") %
                                 { 'modelname': force_unicode(obj._meta.verbose_name), 'name': obj.name, }
                                 )
            return HttpResponseRedirect("%s" % obj.get_absolute_url())
            #return HttpResponseRedirect(request.META['HTTP_REFERER'])
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
        messages.add_message(request, messages.ERROR,
                             _("You cannot delete %(modelname)s \"%(name)s\"") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
        return HttpResponseForbidden()

    if request.method == 'POST':
        geodata.delete()
        messages.add_message(request, messages.SUCCESS,
                             _("Successfully deleted %(modelname)s \"%(name)s\".") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
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


@login_required
def _toggle_recommendation(request, geodatamodel, profile_r, ident):
    geodata = get_object_or_404(geodatamodel, pk=ident)
    profile = request.user.get_profile()

    if request.user == geodata.creator:
        messages.add_message(request, messages.ERROR,
                             _("You cannot recommend %(modelname)s \"%(name)s\".") %
                             { 'modelname': force_unicode(geodata._meta.verbose_name),
                               'name': geodata.name, })
    else:
        if geodata in profile_r.all():
            profile_r.remove(geodata)
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully removed %(modelname)s \"%(name)s\" \
                             from your recommendations.") %
                                 { 'modelname': force_unicode(geodata._meta.verbose_name),
                                   'name': geodata.name, }
                                 )
        else:
            profile_r.add(geodata)
            profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Successfully added %(modelname)s \"%(name)s\" \
                             to your recommendations.") %
                                 { 'modelname': force_unicode(geodata._meta.verbose_name),
                                   'name': geodata.name, }
                                 )
    return HttpResponseRedirect('%s' % geodata.get_absolute_url())

@login_required
def toggle_rec_patrimony(request, ident):
    profile = request.user.get_profile()
    return _toggle_recommendation(request = request,
                                  geodatamodel = EarthGeoDataPatrimony,
                                  profile_r = profile.r_patrimony,
                                  ident = ident)


@login_required
def toggle_rec_construction(request, ident):
    profile = request.user.get_profile()
    return _toggle_recommendation(request = request,
                                  geodatamodel = EarthGeoDataConstruction,
                                  profile_r = profile.r_construction,
                                  ident = ident)


@login_required
def toggle_rec_meeting(request, ident):
    profile = request.user.get_profile()
    return _toggle_recommendation(request = request,
                                  geodatamodel = EarthGeoDataMeeting,
                                  profile_r = profile.r_meeting,
                                  ident = ident)


