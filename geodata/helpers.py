from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.translation import get_language
import json
import urllib


class Nominatim(object):
    search_url = settings.GEODATA_NOMINATIM_SEARCH or \
        'https://nominatim.openstreetmap.org/search?%s'
    reverse_url = settings.GEODATA_NOMINATIM_REVERSE or \
        'https://nominatim.openstreetmap.org/reverse?%s'

    def make_query(self, url, params):
        f = urllib.urlopen(url % urllib.urlencode(params))
        return json.load(f)

    def reverse(self, lat, lon):
        params = {
            'format': 'json',
            'accept-language': get_language(),
            'lat': lat,
            'lon': lon,
            'zoom': 18,
            'addressdetails': 1,
            'email': settings.GEODATA_NOMINATIM_EMAIL
        }
        return self.make_query(self.reverse_url, params)

    def search(self, query):
        params = {
            'format': 'json',
            'accept-language': get_language(),
            'q': smart_str(query),
            'polygon': 0,
            'addressdedtails': 0,
            'email': settings.GEODATA_NOMINATIM_EMAIL
        }
        return self.make_query(self.search_url, params)
