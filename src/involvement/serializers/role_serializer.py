from involvement.models.role import Role
from rest_framework import serializers

#Role serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
