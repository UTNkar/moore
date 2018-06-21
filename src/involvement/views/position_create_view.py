from wagtail.contrib.modeladmin.views import CreateView
from involvement.models import Role


class PositionCreateView(CreateView):
    def get_form(self, form_class=None):
        form = super(PositionCreateView, self).get_form(form_class=form_class)
        queryset = form.fields['role'].queryset
        if not self.request.user.is_superuser:
            queryset = Role.edit_role_types_of(self.request.user)

        queryset = queryset.filter(
            archived=False
        )

        form.fields['role'].queryset = queryset
        return form
