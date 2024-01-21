from rest_framework.permissions import BasePermission

class OwnApplicationPermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """
    def has_object_permission(self, request, view, obj):
        return obj.event_applicant == request.user
