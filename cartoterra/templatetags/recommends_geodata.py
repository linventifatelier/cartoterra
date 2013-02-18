from django import template
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
def recommends_geodata(user, geodata):
    profile = user.get_profile()
    return profile.recommends(geodata)
