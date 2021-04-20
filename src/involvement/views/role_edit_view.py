from wagtail.contrib.modeladmin.views import EditView


class RoleEditView(EditView):
    def get_form(self):
        return super(RoleEditView, self).get_form()
