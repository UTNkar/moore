from rest_framework import serializers
from utils.validators import SSNValidator
from members.models.member import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        depth = 1

class MemberCheckSerializer(serializers.Serializer):
    ssn = serializers.CharField()

    def validate_ssn(self, value):
        SSNValidator()(value)
        return value
