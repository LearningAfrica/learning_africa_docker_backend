from datetime import datetime, timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from utils.permissions import IsOrgAdmin, IsSysAdmin
from.models import Invitation
from .serializers import CreateAdminInvitationSerializer, CreateSuperAdminInvitationSerializer

class SuperAdminInvitationViewSet(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated, IsSysAdmin]

    queryset = Invitation.objects.all()
    serializer_class = CreateSuperAdminInvitationSerializer
        
    def get_serializer_context(self):
        return {
            'user': self.request.user,
            'request': self.request,
        }

class AdminInvitationViewSet(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated, IsOrgAdmin]

    queryset = Invitation.objects.all()
    serializer_class = CreateAdminInvitationSerializer


    def get_serializer_context(self):
        return {
            'user': self.request.user,
            'request': self.request,
        }