from datetime import date
from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.auth import get_permission_codename
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail.core import hooks
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, \
    modeladmin_register
from utils.permissions import RulesPermissionHelper
from events.models import Event, Ticket, Costs, EventApplication

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}">',
        static("css/admin.css")
    )

class EventButtonHelper(ButtonHelper):
    def assign_tickets_button(self, pk, classnames_add, classnames_exclude):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []

        classnames = self.edit_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        text = _('Assign tickets')

        return {
            'url': self.url_helper.get_action_url('assign_tickets', quote(pk)),
            'label': _('Assign tickets'),
            'classname': cn,
            'title': _('Assign applicants to tickets randomly')
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
                            classnames_exclude=None):
        btns = []
        if exclude is None:
            exclude = []
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        ph = self.permission_helper
        usr = self.request.user
        pk = quote(getattr(obj, self.opts.pk.attname))
        btns += super(EventButtonHelper, self).get_buttons_for_obj(
            obj, exclude=exclude, classnames_add=classnames_add,
            classnames_exclude=classnames_exclude)
        btns.append(self.assign_tickets_button(pk, classnames_add, classnames_exclude))
        return btns

class EventAdmin(ModelAdmin):
    model = Event
    menu_label = _('Manage Events')
    menu_icon = 'fa-star'
    menu_order = 100
    permission_helper_class = RulesPermissionHelper
    button_helper_class = EventButtonHelper
    add_to_settings_menu = False
    list_display = ('title', 'description')

class CostsAdmin(ModelAdmin):
    model = Costs
    menu_label = _('Manage price lists')
    menu_icon = 'fa-money'
    menu_order = 200
    permission_helper_class = RulesPermissionHelper
    add_to_settings_menu = False

class TicketAdmin(ModelAdmin):
    model = Ticket
    menu_label = _('Manage tickets')
    menu_icon = 'fa-money'
    menu_order = 300
    list_filter = ('event',)
    permission_helper_class = RulesPermissionHelper
    add_to_settings_menu = False

class EventApplicationAdmin(ModelAdmin):
    model = EventApplication
    menu_label = _('Manage event applications')
    menu_icon = 'fa-money' # TODO
    menu_order = 400
    permission_helper_class = RulesPermissionHelper
    add_to_settings_menu = False

class EventAdminGroup(ModelAdminGroup):
    menu_label = _('Events')
    menu_icon = 'fa-star'
    menu_order = 600
    items = (EventAdmin, CostsAdmin, TicketAdmin, EventApplicationAdmin)

modeladmin_register(EventAdminGroup)
