from wagtail.contrib.modeladmin.views import CreateView
from involvement.models import Role
from involvement.rule_utils import is_super


class PositionCreateView(CreateView):
    def get_form(self):
        form = super(PositionCreateView, self).get_form()
        queryset = form.fields['role'].queryset
        if not is_super(self.request.user):
            queryset = Role.edit_role_types_of(self.request.user)

        queryset = queryset.filter(
            archived=False
        )

        form.fields['role'].queryset = queryset
        return form
