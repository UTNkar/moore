from involvement.models.position import Position
from rest_framework import serializers

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PositionDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        depth = 1
