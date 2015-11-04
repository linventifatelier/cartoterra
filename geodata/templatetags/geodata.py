from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.simple_tag
def world_heritage_logo():
    return '<img alt="world-heritage" width="30" heigth="30" src="%s" onerror="this.src=\'%s\'" />' % (static('img/world_heritage_logo.svg'), static('img/world_heritage_logo.png'))


@register.simple_tag
def unesco_chair_logo():
    return '<img alt="unesco-chair" width="100" src="%s" />' % (static('img/unesco_chair_logo.png'))


@register.filter
def to_leaflet(coords):
    return '[%s, %s]' % (coords[1], coords[0])
