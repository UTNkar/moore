from wagtail.contrib.modeladmin.views import EditView
from involvement.models import Team
from involvement.rules import is_admin


class RoleEditView(EditView):
    def get_form(self, form_class=None):
        form = super(RoleEditView, self).get_form(form_class=form_class)
        if not is_admin(self.request.user):
            form.fields['team'].queryset = Team.official_of(self.request.user)
        return form
