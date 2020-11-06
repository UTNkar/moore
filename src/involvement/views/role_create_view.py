from wagtail.contrib.modeladmin.views import CreateView


class RoleCreateView(CreateView):
    def get_form(self):
        sup = super(RoleCreateView, self)
        return sup.get_form()
