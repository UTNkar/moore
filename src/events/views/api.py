from rest_framework import viewsets
from events.serializers.serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from events.models.costs import Costs
from events.models.event import Event
from events.models.participant import Participant
from events.models.application import EventApplication
from events.models.ticket import Ticket
from events.customPermissions import OwnApplicationPermission

class CostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CostsSerializer
    permission_classes = [AllowAny]
    queryset = Costs.objects.all()

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()

class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Participant.objects.all()

class EventApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = EventApplicationSerializer
    permission_classes = [IsAuthenticated, OwnApplicationPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = EventApplication.objects.filter(event_applicant=user)
        return queryset

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = EventApplication.objects.filter(owner=user)
        return queryset

