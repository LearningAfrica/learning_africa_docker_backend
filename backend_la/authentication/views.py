from rest_framework import status, mixins, permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer, LoginSerializer, RefreshTokenSerializer, ChangePasswordSerializer
from .models import User
from courses.models import OrganizationAdmin, OrganizationInstructor, Organization

class RegisterViewSet(ModelViewSet):
    http_method_names = ['post']

    serializer_class = RegistrationSerializer
    queryset = User.objects.none()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_verified = True
        user.save()

        return Response(user_data, status=status.HTTP_201_CREATED)
    
def get_organizations(user, user_role):
        organizations = []
        if user_role == 'admin':
            admin_orgs = OrganizationAdmin.objects.filter(admin__user=user).prefetch_related('organization').all()
            for admin_org in admin_orgs:
                org_data = {
                    'id': admin_org.organization.id,
                    'name': admin_org.organization.name,
                    'is_active': admin_org.organization.is_active,
                    'position': admin_org.position,
                }
                organizations.append(org_data)
        elif user_role == 'instructor':
            instructor_orgs = OrganizationInstructor.objects.filter(instructor__user=user).prefetch_related('organization').all()
            for instructor_org in instructor_orgs:
                org_data = {
                    'id': instructor_org.organization.id,
                    'name': instructor_org.organization.name,
                    'is_active': instructor_org.organization.is_active,
                }
                organizations.append(org_data)
        return organizations
    
class LoginViewSet(ModelViewSet):
    http_method_names = ['post']

    serializer_class = LoginSerializer
    queryset = User.objects.none()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data

        user_role = user_data.get('user_role')
        id = user_data.get('id')
        user = User.objects.get(id=id)
        
        organizations = get_organizations(user, user_role)
        user_data['organizations'] = organizations
        
        return Response(user_data, status=status.HTTP_200_OK)
    
class RefreshTokenViewSet(ModelViewSet):

    http_method_names = ['post']
    serializer_class = RefreshTokenSerializer

    def create(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            return Response({
                'refresh_token': refresh_token,
                'access_token': access_token
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordViewSet(mixins.UpdateModelMixin, GenericViewSet):
    http_method_names = ['post']
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully"
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)