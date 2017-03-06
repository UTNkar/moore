from datetime import date

from involvement.models import Team, Function, Position, Application
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, \
    modeladmin_register

from django.utils.translation import ugettext_lazy as _

from involvement.rules import is_admin
from utils.permissions import RulesPermissionHelper


class TeamAdmin(ModelAdmin):
    model = Team
    menu_icon = 'group'
    menu_order = 100
    list_display = ('name_en', 'name_sv', 'email')
    search_fields = ('name_en', 'name_sv', 'description_en', 'description_sv',
                     'leader_en', 'leader_sv', 'email')
    permission_helper_class = RulesPermissionHelper

    def get_queryset(self, request):
        if is_admin(request.user):
            return super().get_queryset(request)
        else:
            # TODO : Is this efficient?
            applications = Application.objects.filter(
                applicant=request.user,
                status='appointed',
                position__term_from__lte=date.today(),
                position__term_to__gte=date.today(),
                position__function__official=True,
                position__function__team_id__isnull=False,
            ).select_related('position__function__team')
            teams = []
            for i in applications:
                teams.append(i.position.function.team.id)
            qs = Team.objects.filter(id__in=teams)
            ordering = self.get_ordering(request)
            if ordering:
                qs = qs.order_by(*ordering)
            return qs


class FunctionAdmin(ModelAdmin):
    model = Function
    menu_icon = 'user'
    menu_order = 200
    list_display = ('team', 'name_en', 'name_sv', 'archived')
    search_fields = ('name_en', 'name_sv', 'description_en',
                     'description_sv')
    permission_helper_class = RulesPermissionHelper

    def get_queryset(self, request):
        if is_admin(request.user):
            return super().get_queryset(request)
        else:
            # TODO : Is this efficient?
            applications = Application.objects.filter(
                applicant=request.user,
                status='appointed',
                position__term_from__lte=date.today(),
                position__term_to__gte=date.today(),
                position__function__official=True,
                position__function__team_id__isnull=False,
            ).select_related('position__function__team')
            teams = []
            for i in applications:
                teams.append(i.position.function.team)
            qs = Function.objects.filter(team__in=teams)
            ordering = self.get_ordering(request)
            if ordering:
                qs = qs.order_by(*ordering)
            return qs


class PositionAdmin(ModelAdmin):
    model = Position
    menu_icon = 'search'
    menu_order = 300
    list_display = ('function', 'appointments', 'term_from', 'term_to')
    search_fields = ('comments_en', 'comments_sv')
    list_filter = ('term_from', 'term_to')
    permission_helper_class = RulesPermissionHelper

    def get_queryset(self, request):
        if is_admin(request.user):
            return super().get_queryset(request)
        else:
            # TODO : Is this efficient?
            applications = Application.objects.filter(
                applicant=request.user,
                status='appointed',
                position__term_from__lte=date.today(),
                position__term_to__gte=date.today(),
                position__function__official=True,
                position__function__team_id__isnull=False,
            ).select_related('position__function__team')
            teams = []
            for i in applications:
                teams.append(i.position.function.team)
            qs = Position.objects.filter(function__team__in=teams)
            ordering = self.get_ordering(request)
            if ordering:
                qs = qs.order_by(*ordering)
            return qs


class ApplicationAdmin(ModelAdmin):
    model = Application
    menu_icon = 'mail'
    menu_order = 400
    list_display = ('position', 'applicant', 'status')
    permission_helper_class = RulesPermissionHelper


class InvolvementAdminGroup(ModelAdminGroup):
    menu_label = _('Involvement')
    menu_icon = 'group'
    menu_order = 500
    items = (TeamAdmin, FunctionAdmin, PositionAdmin, ApplicationAdmin)


modeladmin_register(InvolvementAdminGroup)
