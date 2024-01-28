from rest_framework import viewsets
from involvement.serializers.team_serializer import TeamSerializer
from rest_framework.permissions import AllowAny
from involvement.models.team import Team
from src.customPermissions import CsrfExemptSessionAuthentication
#Read Teams API
class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [AllowAny, CsrfExemptSessionAuthentication]
    queryset = Team.objects.all()

