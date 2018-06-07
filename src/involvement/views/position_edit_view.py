from wagtail.contrib.modeladmin.views import EditView
from involvement.models import Role, Team
from involvement.rules import is_admin


class PositionEditView(EditView):
    def get_form(self, form_class=None):
        form = super(PositionEditView, self).get_form(form_class=form_class)
        queryset = form.fields['role'].queryset
        init = Role.objects.get(pk=form.initial['role'])
        if not init.archived:
            queryset = queryset.filter(
                archived=False
            )
        if not is_admin(self.request.user):
            teams = Team.official_of(self.request.user)
            queryset = queryset.filter(
                team__in=teams
            )
        form.fields['role'].queryset = queryset
        return form
