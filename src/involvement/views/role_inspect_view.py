from wagtail.contrib.modeladmin.views import InspectView


class RoleInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super(RoleInspectView, self).get_context_data(**kwargs)
        context['current_applications'] = self.get_current_applications
        context['old_applications'] = self.get_old_applications
        return context

    def get_current_applications(self):
        applications = []
        for position in self.instance.current_positions:
            applications.extend(position.applications.filter(
                status='appointed'
            ))

        return applications

    def get_old_applications(self):
        applications = []
        for position in self.instance.old_positions:
            applications.extend(position.applications.filter(
                status='appointed'
            ))
        return applications
