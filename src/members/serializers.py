from rest_framework import serializers
from utils.validators import SSNValidator


class MemberCheckSerializer(serializers.Serializer):
    ssn = serializers.CharField()

    def validate_ssn(self, value):
        SSNValidator()(value)
        return value
