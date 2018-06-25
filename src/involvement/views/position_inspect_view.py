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
        return self.instance.applications.filter(
            status='submitted'
        )
