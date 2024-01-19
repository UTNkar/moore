from involvement.models.application import Application
from rest_framework import serializers

#Role serializer
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        depth = 1

