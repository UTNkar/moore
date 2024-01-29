from rest_framework import viewsets, authentication, mixins
from events.serializers.serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from events.models.costs import Costs
from events.models.event import Event
from events.models.participant import Participant
from events.models.application import EventApplication
from events.models.ticket import Ticket
from events.customPermissions import OwnApplicationPermission, CsrfExemptSessionAuthentication, \
    ParticipantAllowancePermission

class CostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CostsSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [AllowAny]
    queryset = Costs.objects.all()

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()

class ParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipantSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticatedOrReadOnly, ParticipantAllowancePermission]

    def get_queryset(self):
        user = self.request.user
        tickets = list(Ticket.objects.filter.values_list(owner=user))
        queryset = Participant.objects.filter(ticket__in=tickets)
        return queryset

class EventApplicationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, \
                              mixins.DestroyModelMixin):
    serializer_class = EventApplicationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticated, OwnApplicationPermission]

    def get_queryset(self):
        user = self.request.user
        if self.action in ['retrieve', 'list']:
            queryset = EventApplication.objects.filter(event_applicant=user)
        else:
            queryset = EventApplication.objects.all()
        return queryset

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(owner=user)
        return queryset

