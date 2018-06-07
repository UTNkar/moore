from wagtail.contrib.modeladmin.views import InspectView


class PositionInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super(PositionInspectView, self).get_context_data(**kwargs)
        applicants = self.instance.applications.all()
        if self.instance.current_action() == 'done':
            context['applicants'] = applicants.filter(status='appointed')
        else:
            context['applicants'] = applicants.exclude(
                status__in=['disapproved', 'turned_down']
            )
        return context
