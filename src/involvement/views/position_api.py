from rest_framework import viewsets
from involvement.serializers.position_serializer import PositionSerializer
from rest_framework.permissions import AllowAny
from involvement.models.position import Position

class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    permission_classes = [AllowAny]
    queryset = Position.objects.all()

