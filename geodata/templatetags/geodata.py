from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.filter
def to_leaflet(coords):
    return '[%s, %s]' % (coords[1], coords[0])
