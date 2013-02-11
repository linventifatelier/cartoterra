from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from geodata.helpers import Nominatim


@dajaxice_register
def search_nominatim(request, search_terms):
    dajax = Dajax()
    n = Nominatim()
    results = n.search(search_terms)
    print results
    out = []
    for place in results:
        bboxlist = place.get('boundingbox', [])
        if len(bboxlist) >= 4:
            minlat, maxlat, minlon, maxlon = bboxlist[:4]
        else:
            bboxstr = ""
        out.append("<option value='%(name)s' lat='%(lat)s' lon='%(lon)s' minlat='%(minlat)s' maxlat='%(maxlat)s' minlon='%(minlon)s' maxlon='%(maxlon)s'>%(name)s, %(lat)s:%(lon)s</option>" %
                   { 'name' : place.get('display_name'), 'lat': place.get('lat', "0"), 'lon': place.get('lon', "0"), 'minlat': minlat, 'maxlat': maxlat, 'minlon': minlon, 'maxlon': maxlon, })
        #out.append("<option value='%(name)s'>%(name)s</option>" %
        #          { 'name' : place.get('display_name'), 'lat': place.get('lat', "0"), 'lon': place.get('lon', "0")})
    dajax.assign('#search_results', 'innerHTML', ''.join(out))
    dajax.script('$("#spin").spin(false);')
    return dajax.json()


@dajaxice_register
def get_point_coordinates(request, lat, lon, minlat, maxlat, minlon, maxlon):
    dajax = Dajax()
    #dajax.script('module.map.zoomToExtent(new OpenLayers.Bounds(%s));' % bbox)
    dajax.assign('#latitude', 'value', lat)
    dajax.assign('#longitude', 'value', lon)
    dajax.script('panToLatLonBoundingBox(%(lat)s, %(lon)s, %(minlat)s, %(maxlat)s, %(minlon)s, %(maxlon)s);' % { 'lat': lat, 'lon': lon, 'minlat': minlat, 'maxlat': maxlat, 'minlon': minlon, 'maxlon': maxlon })
    #dajax.script('panToLatLonBoundingBox(44.3239145, 3.59404, 44.2790718078613, 44.3588905334473, 3.5451807975769, 3.63086891174316);')
    return dajax.json()
