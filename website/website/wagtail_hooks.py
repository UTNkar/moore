from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, \
    ThumbnailMixin

from website.models import Logo


class LogoAdmin(ThumbnailMixin, ModelAdmin):
    model = Logo
    menu_icon = 'picture'
    menu_order = 1000
    list_display = ('admin_thumb', 'category', 'link')
    add_to_settings_menu = True
    thumb_image_field_name = 'logo'
    thumb_image_filter_spec = 'fill-128x128'


modeladmin_register(LogoAdmin)
