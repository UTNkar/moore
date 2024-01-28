from rest_framework import viewsets, authentication
from involvement.serializers.role_serializer import RoleSerializer
from rest_framework.permissions import AllowAny
from involvement.models.role import Role
from involvement.customPermissions import CsrfExemptSessionAuthentication
#Role view
class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoleSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [AllowAny]
    queryset = Role.objects.all()
