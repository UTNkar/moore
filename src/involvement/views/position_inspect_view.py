from wagtail.contrib.modeladmin.views import InspectView


class PositionInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super(PositionInspectView, self).get_context_data(**kwargs)
        context['appointed_applications'] = self.get_appointed_applications
        context['submitted_applications'] = self.get_submitted_applications
        return context

    def get_appointed_applications(self):
        return self.instance.applications.filter(
            status='appointed'
        )

    def get_submitted_applications(self):
        # Since roles that arent role type styrelse or fum get automatically
        # set to approved we need to show applications with status approved
        # when inspecting a role. This is a temporary fix.
        return self.instance.applications.filter(
            status__in=['submitted', 'approved']
        )
