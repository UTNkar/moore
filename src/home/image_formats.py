from wagtail.images.formats import Format, register_image_format

from django.utils.translation import gettext_lazy as _

register_image_format(Format(
    'center',
    _('Centered'),
    'richtext-image center',
    'original'
))
