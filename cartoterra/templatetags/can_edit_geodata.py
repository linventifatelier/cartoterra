from django import template
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
def can_edit_geodata(user, geodata):
    if user.is_authenticated():
        return (geodata.creator == user or user.is_staff)
    else:
        return False
