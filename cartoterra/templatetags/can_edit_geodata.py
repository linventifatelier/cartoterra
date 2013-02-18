from django import template
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
def can_edit_geodata(user, geodata):
    if user.is_authenticated():
        if geodata.creator == user:
            return True
        else:
            return False
    else:
        return False
