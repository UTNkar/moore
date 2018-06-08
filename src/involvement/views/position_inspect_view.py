from wagtail.contrib.modeladmin.views import InspectView


class PositionInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super(PositionInspectView, self).get_context_data(**kwargs)
        context['current_mandates'] = self.get_mandates
        context['submitted_applications'] = self.get_submitted_applications
        return context

    def get_mandates(self):
        return self.instance.current_mandates.all()

    def get_submitted_applications(self):
        self.instance.applications.filter(
            status='submitted'
        )
