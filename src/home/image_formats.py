from wagtail.wagtailimages.formats import Format, register_image_format

from django.utils.translation import ugettext_lazy as _

register_image_format(Format(
    'center',
    _('Centered'),
    'richtext-image center',
    'original'
))
