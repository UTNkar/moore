from rest_framework import viewsets
from involvement.serializers.role_serializer import RoleSerializer
from rest_framework.permissions import AllowAny
from involvement.models.role import Role

#Role view
class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    queryset = Role.objects.all()
