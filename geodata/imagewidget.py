"""Admin image widget."""
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class AdminImageWidget(AdminFileWidget):
    """Admin image widget."""
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(" <a href=\"%s\" target=\"_blank\">\
                <img src=\"%s\" alt=\"%s\" /></a> %s " %
                          (image_url, image_url, file_name, _('Change:')))
            output.append(
                super(AdminImageWidget, self).render(name, value, attrs)
            )
            return mark_safe("".join(output))
