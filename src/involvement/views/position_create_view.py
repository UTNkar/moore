from wagtail.contrib.modeladmin.views import CreateView
from involvement.models import Role
from involvement.rule_utils import is_admin


class PositionCreateView(CreateView):
    def get_form(self, form_class=None):
        form = super(PositionCreateView, self).get_form(form_class=form_class)
        queryset = form.fields['role'].queryset
        if not is_admin(self.request.user):
            queryset = Role.edit_permission_of(self.request.user)

        queryset = queryset.filter(
            archived=False
        )

        form.fields['role'].queryset = queryset
        return form
