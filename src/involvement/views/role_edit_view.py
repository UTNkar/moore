from wagtail.contrib.modeladmin.views import EditView


class RoleEditView(EditView):
    def get_form(self, form_class=None):
        return super(RoleEditView, self).get_form(form_class=form_class)
