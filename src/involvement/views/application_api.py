from rest_framework import viewsets
from involvement.serializers.application_serializer import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from involvement.models.application import Application

#Role view
class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.filter(applicant=user)
        return queryset
