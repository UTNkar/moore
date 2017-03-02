from involvement.models import Team, Function, Position, Application
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, \
    modeladmin_register

from django.utils.translation import ugettext_lazy as _


class TeamAdmin(ModelAdmin):
    model = Team
    menu_icon = 'group'
    menu_order = 100
    list_display = ('name_en', 'name_sv', 'email')
    search_fields = ('name_en', 'name_sv', 'description_en', 'description_sv',
                     'leader_en', 'leader_sv', 'email')


class FunctionAdmin(ModelAdmin):
    model = Function
    menu_icon = 'user'
    menu_order = 200
    list_display = ('team', 'name_en', 'name_sv', 'archived')
    search_fields = ('name_en', 'name_sv', 'description_en',
                     'description_sv')


class PositionAdmin(ModelAdmin):
    model = Position
    menu_icon = 'search'
    menu_order = 300
    list_display = ('function', 'appointments', 'term_from', 'term_to')
    search_fields = ('comments_en', 'comments_sv')
    list_filter = ('term_from', 'term_to')


class ApplicationAdmin(ModelAdmin):
    model = Application
    menu_icon = 'mail'
    menu_order = 400
    list_display = ('position', 'applicant', 'status')


class InvolvementAdminGroup(ModelAdminGroup):
    menu_label = _('Involvement')
    menu_icon = 'group'
    menu_order = 500
    items = (TeamAdmin, FunctionAdmin, PositionAdmin, ApplicationAdmin)


modeladmin_register(InvolvementAdminGroup)
