from rest_framework import viewsets, mixins, authentication
from involvement.serializers.application_serializer import ApplicationSerializer, ApplicationEditSerializer
from rest_framework.permissions import IsAuthenticated
from involvement.models.application import Application
from involvement.customPermissions import OwnApplicationPermission, DeleteApplicationPermission, \
    EditApplicationPermission
from involvement.customPermissions import CsrfExemptSessionAuthentication

#Role view
class ApplicationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, \
                         mixins.RetrieveModelMixin):
    serializer_class = ApplicationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticated, OwnApplicationPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.filter(applicant=user)
        return queryset

class ApplicationDeleteViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin):
    serializer_class = ApplicationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticated, OwnApplicationPermission, DeleteApplicationPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.filter(applicant=user)
        return queryset

class ApplicationEditViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = ApplicationEditSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, authentication.BasicAuthentication)
    permission_classes = [IsAuthenticated, OwnApplicationPermission, EditApplicationPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.filter(applicant=user)
        return queryset
