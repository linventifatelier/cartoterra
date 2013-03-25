from django import template
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
def recommends_geodata(user, geodata):
    return user.profile.recommends(geodata)
