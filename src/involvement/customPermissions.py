from rest_framework.permissions import BasePermission
from rest_framework.authentication import SessionAuthentication
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return
class ReadAndCreate(BasePermission):
    """
        Authenticated user can create but not delete or update.
    """
    def has_permission(self, request, view):
        return True if request.method in ["GET", "HEAD", "OPTIONS", "POST"] else False

class ReadCreateUpdate(BasePermission):
    """
        Authenticated user can create and update but not delete.
    """
    def has_permission(self, request, view):
        return True if request.method not in ["DELETE"] else False

class OwnApplicationPermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """
    def has_object_permission(self, request, view, obj):
        return obj.applicant == request.user
