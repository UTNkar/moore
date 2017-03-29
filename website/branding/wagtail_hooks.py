from wagtail.contrib.modeladmin.options import ModelAdmin, \
    modeladmin_register, ThumbnailMixin, ModelAdminGroup
from django.utils.translation import ugettext_lazy as _

from branding.models import Logo


class LogoAdmin(ThumbnailMixin, ModelAdmin):
    model = Logo
    menu_icon = 'picture'
    menu_order = 100
    list_display = ('admin_thumb', 'category', 'link')
    thumb_image_field_name = 'logo'
    thumb_image_filter_spec = 'fill-128x128'


class BrandingAdminGroup(ModelAdminGroup):
    menu_label = _('Branding')
    menu_icon = 'picture'
    menu_order = 600
    items = (LogoAdmin,)


modeladmin_register(BrandingAdminGroup)
