from rest_framework import viewsets
from events.serializers.serializers import *
from rest_framework.permissions import AllowAny
from events.models.costs import Costs
from events.models.event import Event
from events.models.participant import Participant
from events.models.application import EventApplication
from events.models.ticket import Ticket

class CostsViewSet(viewsets.ModelViewSet):
    serializer_class = CostsSerializer
    permission_classes = [AllowAny]
    queryset = Costs.objects.all()

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    queryset = Event.objects.all()

class ParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [AllowAny]
    queryset = Participant.objects.all()

class EventApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = EventApplicationSerializer
    permission_classes = [AllowAny]
    queryset = EventApplication.objects.all()

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]
    queryset = Ticket.objects.all()

