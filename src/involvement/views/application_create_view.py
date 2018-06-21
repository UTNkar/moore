from wagtail.contrib.modeladmin.views import CreateView
from involvement.models import Role
from involvement.rule_utils import is_admin


class ApplicationCreateView(CreateView):
    def get_form(self, form_class=None):
        form = super(ApplicationCreateView, self) \
            .get_form(form_class=form_class)

        if not self.request.user.is_superuser \
                and not is_admin(self.request.user):
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
            roles = Role.edit_role_types_of(self.request.user)
            position_qs = position_qs.filter(role__in=roles)
            form.fields['position'].queryset = position_qs

        return form
