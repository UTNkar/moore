from wagtail.contrib.modeladmin.views import CreateView


class RoleCreateView(CreateView):
    def get_form(self, form_class=None):
        return super(RoleCreateView, self).get_form(form_class=form_class)
