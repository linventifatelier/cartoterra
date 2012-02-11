## from django.contrib.admin.widgets import AdminFileWidget
## from django.utils.translation import ugettext as _
## from django.utils.safestring import mark_safe
## import os
## import Image

## class AdminImageWidget(AdminFileWidget):
##   def render(self, name, value, attrs=None):
##     output = []
##     if value and getattr(value, "url", None):

##       image_url = value.url
##       file_name=str(value)

##       # defining the size
##       size='100x100'
##       x, y = [int(x) for x in size.split('x')]

##       # defining the filename and the miniature filename
##       filehead, filetail  = os.path.split(value.path)
##       basename, format  = os.path.splitext(filetail)
##       miniature     = basename + '_' + size + format
##       filename    = value.path
##       miniature_filename  = os.path.join(filehead, miniature)
##       filehead, filetail  = os.path.split(value.url)
##       miniature_url     = filehead + '/' + miniature

##       # make sure that the thumbnail is a version of the current original sized image
##       if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
##         os.unlink(miniature_filename)

##       # if the image wasn't already resized, resize it
##       if not os.path.exists(miniature_filename):
##         image = Image.open(filename)
##         image.thumbnail([x, y], Image.ANTIALIAS)
##         try:
##           image.save(miniature_filename, image.format, quality=100, optimize=1)
##         except:
##           image.save(miniature_filename, image.format, quality=100)

##       output.append(u' <div><a href="%s" target="_blank"><img src="%s" alt="%s" /></a></div> %s ' % \
##       (miniature_url, miniature_url, miniature_filename, _('Change:')))

##     output.append(super(AdminFileWidget, self).render(name, value, attrs))
##     return mark_safe(u''.join(output))


from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget):
  def render(self, name, value, attrs=None):
    output = []
    if value and getattr(value, "url", None):
      image_url = value.url
      file_name=str(value)
      output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a> %s ' % \
                  (image_url, image_url, file_name, _('Change:')))
      output.append(super(AdminFileWidget, self).render(name, value, attrs))
    return mark_safe(u''.join(output))
