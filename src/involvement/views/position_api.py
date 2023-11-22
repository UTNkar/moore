from rest_framework import viewsets
from involvement.serializers.position_serializer import PositionSerializer, PositionDepthSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from involvement.models.position import Position

class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Position.objects.all()

class Position2ViewSet(viewsets.ModelViewSet):
    serializer_class = PositionDepthSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Position.objects.all()
