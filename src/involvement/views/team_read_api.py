from rest_framework import viewsets, authentication
from involvement.serializers.team_serializer import TeamSerializer
from rest_framework.permissions import AllowAny
from involvement.models.team import Team
from involvement.customPermissions import CsrfExemptSessionAuthentication
#Read Teams API
class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [AllowAny]
    queryset = Team.objects.all()

