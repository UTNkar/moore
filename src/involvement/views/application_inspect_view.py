from wagtail.contrib.modeladmin.views import InspectView


class ApplicationInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super(ApplicationInspectView, self) \
            .get_context_data(**kwargs)
        return context
