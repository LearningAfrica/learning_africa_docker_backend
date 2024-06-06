from django.db import models
from shortuuid.django_fields import ShortUUIDField
from datetime import datetime, timedelta

class Invitation(models.Model):
    USER_TYPE_CHOICES = [
        ('adm', 'Admin'),
        ('ins', 'Instructor'),
        ('stu', 'Student'),
    ]

    organization_uuid = ShortUUIDField(length=12, max_length=12, editable=False, blank=True, null=True)
    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES)
    is_used = models.BooleanField(default=False)
    token = models.CharField(max_length=500)
    expiration_time = models.DateTimeField()

    class Meta:
        db_table = 'invitations'

    def is_expired(self):
        return datetime.utcnow() > self.expiration_time
    
    def is_admin_invitation(self):
        return self.user_type == 'adm'
    