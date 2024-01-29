from rest_framework.permissions import BasePermission
from rest_framework.authentication import SessionAuthentication
from datetime import datetime
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return

class OwnApplicationPermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """
    def has_object_permission(self, request, view, obj):
        if obj.event.end_of_application < datetime.now():
            return False
        return obj.event_applicant == request.user

class ParticipantAllowancePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in ["GET", "HEAD", "OPTIONS"]:
            return not obj.ticket.locked
        else:
            return True
