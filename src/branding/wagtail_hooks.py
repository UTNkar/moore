from wagtail.contrib.modeladmin.options import ModelAdmin, \
    modeladmin_register, ThumbnailMixin, ModelAdminGroup
from django.utils.translation import ugettext_lazy as _

from branding.models import Logo, Instagram


class LogoAdmin(ThumbnailMixin, ModelAdmin):
    model = Logo
    menu_icon = 'fa-rebel'
    menu_order = 100
    list_display = ('admin_thumb', 'category', 'link')
    thumb_image_field_name = 'logo'
    thumb_image_filter_spec = 'fill-128x128'


class InstagramAdmin(ModelAdmin):
    model = Instagram
    menu_icon = 'fa-instagram'
    menu_order = 110


class BrandingAdminGroup(ModelAdminGroup):
    menu_label = _('Branding')
    menu_icon = 'fa-paint-brush'
    menu_order = 600
    items = (LogoAdmin, InstagramAdmin)


modeladmin_register(BrandingAdminGroup)
