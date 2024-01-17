from involvement.models.team import Team
from rest_framework import serializers

#Serializer for team
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

