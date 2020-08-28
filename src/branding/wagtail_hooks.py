from wagtail.contrib.modeladmin.options import ModelAdmin, \
    modeladmin_register, ThumbnailMixin, ModelAdminGroup
from django.utils.translation import ugettext_lazy as _

from branding.models import Logo, InstagramFeed


class LogoAdmin(ThumbnailMixin, ModelAdmin):
    model = Logo
    menu_icon = 'fa-rebel'
    menu_order = 100
    list_display = ('admin_thumb', 'category', 'link')
    thumb_image_field_name = 'logo'
    thumb_image_filter_spec = 'fill-128x128'


class InstagramFeedAdmin(ModelAdmin):
    model = InstagramFeed
    menu_icon = 'fa-instagram'
    menu_order = 110
    create_template_name = "instagramfeed/create.html"


class BrandingAdminGroup(ModelAdminGroup):
    menu_label = _('Branding')
    menu_icon = 'fa-paint-brush'
    menu_order = 600
    items = (LogoAdmin, InstagramFeedAdmin)


modeladmin_register(BrandingAdminGroup)
