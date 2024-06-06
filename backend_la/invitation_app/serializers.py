from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import serializers

from .models import Invitation
from utils.send_email_util import Util
from utils.jwt_utils import encode_token

class CreateSuperAdminInvitationSerializer(serializers.ModelSerializer):

    receiver_name = serializers.CharField(max_length=50, write_only=True)
    receiver_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Invitation
        fields = ['id','receiver_name', 'receiver_email']

    def create(self, validated_data):
        user = self.context['user']
        receiver_name = validated_data.pop('receiver_name')
        receiver_email = validated_data.pop('receiver_email')

        user_type = 'adm'

        payload = {
            'user_type': user_type
        }

        token = encode_token(payload)
        expiration_time = datetime.utcnow() + timedelta(days=2)

        invitation = Invitation.objects.create(
            user_type=user_type,
            token=token,
            expiration_time=expiration_time
        )
        
        domain = "https://learning-africa-test.netlify.app/invite/register"
        invitation_link = f"{domain}?token={token}"

        if user_type == 'adm':
            join_as = 'Adminstrator'
            subject = 'Admin Invitation Link'
            sender_name = f"{user.first_name} {user.last_name}"
            email_body = f'Hello {receiver_name}, you have been invited to Learning Africa by {sender_name}. \nPlease join as {join_as} using link below:\n {invitation_link}\nThis link is active for 2 days.'
            admin_data = {
                'email_body':email_body,
                'to_email': receiver_email,
                'email_subject': subject
                }
            Util.send_email(admin_data)
        else:
            return serializers.ValidationError({'error': 'Only admins can be invited using this link.'})

        return invitation

class CreateAdminInvitationSerializer(serializers.ModelSerializer):

    receiver_name = serializers.CharField(max_length=50, write_only=True)
    receiver_email = serializers.EmailField(write_only=True)
    organization_uuid = serializers.CharField()

    class Meta:
        model = Invitation
        fields = ['id','receiver_name', 'organization_uuid', 'user_type', 'receiver_email']

    def create(self, validated_data):
        user = self.context['user']
        user_type = validated_data.get('user_type')
        organization_uuid = validated_data.get('organization_uuid')
        receiver_name = validated_data.pop('receiver_name')
        receiver_email = validated_data.pop('receiver_email')

        payload = {
            'org': organization_uuid,
            'user_type': user_type
        }

        token = encode_token(payload)
        expiration_time = datetime.utcnow() + timedelta(days=2)

        invitation = Invitation.objects.create(
            organization_uuid=organization_uuid,
            user_type=user_type,
            token=token,
            expiration_time=expiration_time
        )

        domain = "https://learning-africa-test.netlify.app/invite/register"
        invitation_link = f"{domain}?token={token}"

        if user_type == 'ins':
            join_as = 'Instructor'
            subject = 'Instructor Invitation Link'
            sender_name = f"{user.first_name} {user.last_name}"
            email_body = f'Hello {receiver_name}, you have been invited to Learning Africa by {sender_name}. \nPlease join as {join_as} using link below:\n {invitation_link}\nThis link is active for 2 days.'
            instructor_data = {
                'email_body':email_body,
                'to_email': receiver_email,
                'email_subject': subject
                }
            Util.send_email(instructor_data)
        elif user_type == 'stu':
            join_as = 'Learner'
            subject = 'Learner Invitation Link'
            sender_name = f"{user.first_name} {user.last_name}"
            email_body = f'Hello {receiver_name}, you have been invited to Learning Africa by {sender_name}. \nPlease join as {join_as} using link below:\n {invitation_link}\nThis link is active for 2 days.'
            student_data = {
                'email_body':email_body,
                'to_email': receiver_email,
                'email_subject': subject
                }
            Util.send_email(student_data)

        return invitation