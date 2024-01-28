from rest_framework import viewsets, authentication, mixins
from involvement.serializers.position_serializer import PositionSerializer, PositionDepthSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from involvement.models.position import Position
from involvement.customPermissions import CsrfExemptSessionAuthentication

class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PositionSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Position.objects.all()

class Position2ViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PositionDepthSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Position.objects.all()
