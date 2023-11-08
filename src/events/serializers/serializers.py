from events.models.costs import Costs
from events.models.event import Event
from events.models.participant import Participant
from events.models.application import EventApplication
from events.models.ticket import Ticket
from rest_framework import serializers

class CostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Costs

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant

class EventApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventApplication

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
