from rest_framework import viewsets
from events.serializers.serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from events.models.costs import Costs
from events.models.event import Event
from events.models.participant import Participant
from events.models.application import EventApplication
from events.models.ticket import Ticket
from events.customPermissions import OwnApplicationPermission
from src.customPermissions import CsrfExemptSessionAuthentication

class CostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CostsSerializer
    permission_classes = [AllowAny, CsrfExemptSessionAuthentication]
    queryset = Costs.objects.all()

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CsrfExemptSessionAuthentication]
    queryset = Event.objects.all()

class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CsrfExemptSessionAuthentication]
    queryset = Participant.objects.all()

class EventApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = EventApplicationSerializer
    permission_classes = [IsAuthenticated, OwnApplicationPermission, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        user = self.request.user
        queryset = EventApplication.objects.filter(event_applicant=user)
        return queryset

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        user = self.request.user
        queryset = EventApplication.objects.filter(owner=user)
        return queryset

