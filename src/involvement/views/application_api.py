from rest_framework import viewsets, mixins
from involvement.serializers.application_serializer import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from involvement.models.application import Application
from involvement.customPermissions import OwnApplicationPermission

#Role view
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, OwnApplicationPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.filter(applicant=user)
        return queryset


