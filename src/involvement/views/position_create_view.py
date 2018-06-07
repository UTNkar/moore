from wagtail.contrib.modeladmin.views import CreateView
from involvement.models import Team
from involvement.rules import is_admin


class PositionCreateView(CreateView):
    def get_form(self, form_class=None):
        form = super(PositionCreateView, self).get_form(form_class=form_class)
        queryset = form.fields['role'].queryset
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
