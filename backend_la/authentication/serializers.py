from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from jose import jwt
import uuid

from .models import User
from .backends import EmailUsernameAuthenticationBackend as EoU
from utils.jwt_utils import decode_token

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    id = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    invitation_token = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_super_admin', 'is_admin', 'is_instructor', 'is_student', 'invitation_token']

    def validate(self, attrs):
        email = attrs.get('email', '')
        invitation_token = attrs.get('invitation_token', None)

        if invitation_token:
            try:
                decode_payload = decode_token(invitation_token)
            except jwt.JWTError:
                raise serializers.ValidationError('Invalid invitation token')
        return attrs
    
    def create(self, validated_data):
        is_super_admin = validated_data.get('is_super_admin')
        is_admin = validated_data.get('is_admin')
        is_instructor = validated_data.get('is_instructor')
        is_student = validated_data.get('is_student')
        invitation_token = validated_data.pop('invitation_token', None)

        if invitation_token:
            try:
                decode_payload = decode_token(invitation_token)
                organization_uuid = decode_payload.get('organization_uuid')
                user_type = decode_payload.get('user_type')
            except jwt.JWTError:
                raise serializers.ValidationError({'error': 'Invalid invitation token'})
            
            if user_type == 'ins':
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
                # user = User.objects.create_instructor(**validated_data)
            elif user_type == 'adm':
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
            elif user_type == 'stu':
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
        else:
            if is_super_admin == True:
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
            elif is_admin == True:
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
            elif is_instructor == True:
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
            elif is_student == True:
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
            else:
                email = validated_data.get('email', None)
                if email:
                    try:
                        user = User.objects.get(email=email)
                        if user:
                            raise serializers.ValidationError({'error': 'User with this email already exists'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(**validated_data)
        
        return user

class LoginSerializer(serializers.ModelSerializer):
    username_or_email = serializers.CharField(max_length=255, required=False)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    user_role = serializers.CharField(max_length=50, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    # organizations = serializers.SerializerMethodField(method_name='get_organizations')

    class Meta:
        model = User
        fields = ['id', 'username_or_email', 'username', 'password', 'user_role', 'refresh_token', 'access_token']

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email', '')
        password = attrs.get('password', '')

        user = EoU.authenticate(username=username_or_email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid username or password, try again.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        tokens = user.tokens()
        refresh = tokens['refresh']
        access = tokens['access']

        if user.is_super_admin == True:
            user_role = 'super_admin'
        elif user.is_admin == True:
            user_role = 'admin'
        elif user.is_instructor == True:
            user_role = 'instructor'
        elif user.is_student == True:
            user_role = 'student'
        else:
            user_role = None
        

        return {
            'id': user.id,
            'user_role': user_role,
            'username': user.username,
            'refresh_token': refresh,
            'access_token': access }
    
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=1000)

class ChangePasswordSerializer(serializers.Serializer):

    model = User

    old_password = serializers.CharField(max_length=68, required=True)
    new_password = serializers.CharField(max_length=68, required=True)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']