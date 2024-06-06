from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4
from shortuuid.django_fields import ShortUUIDField

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_super_admin(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_author', False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_admin(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', True)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_instructor(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_instructor', True)
        return self._create_user(username, email, password, **extra_fields)
    

    def create_student(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_student', True)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self._create_user(username, email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }