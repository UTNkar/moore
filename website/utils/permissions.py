from django.contrib.auth import get_permission_codename
from wagtail.contrib.modeladmin.helpers import PermissionHelper


class RulesPermissionHelper(PermissionHelper):
    """Wagtail Permission helper using rules permissions."""
    def user_can_list(self, user):
        opts = self.opts
        codename = get_permission_codename('list', opts)
        return user.has_perm('%s.%s' % (opts.app_label, codename))

    def user_can_edit_obj(self, user, obj):
        opts = self.opts
        codename = get_permission_codename('change', opts)
        return user.has_perm('%s.%s' % (opts.app_label, codename), obj)

    def user_can_delete_obj(self, user, obj):
        opts = self.opts
        codename = get_permission_codename('delete', opts)
        return user.has_perm('%s.%s' % (opts.app_label, codename), obj)
