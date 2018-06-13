from wagtail.contrib.modeladmin.views import EditView
from involvement.models import Role
from involvement.rule_utils import is_admin


class ApplicationEditView(EditView):
    def get_form(self, form_class=None):
        form = super(ApplicationEditView, self).get_form(form_class=form_class)

        if not is_admin(self.request.user):
            # Filter status
            form.fields['status'].choices = form.fields['status'].choices[1:]
            accepted_choices = ['submitted', 'approved', 'disapproved']
            filtered_choices = []
            for choice in form.fields['status'].choices:
                if choice[0] in accepted_choices:
                    filtered_choices.append(choice)
            form.fields['status'].choices = filtered_choices

            # Filter position
            position_qs = form.fields['position'].queryset
            roles = Role.edit_permission_of(self.request.user)
            position_qs = position_qs.filter(role__in=roles)
            form.fields['position'].queryset = position_qs

        return form
