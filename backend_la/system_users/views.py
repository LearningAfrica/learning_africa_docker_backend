from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions
from utils.pagination import DefaultPagination

from .models import SuperAdmin, Admin, Instructor, Student
from .serializers import SuperAdminSerializer, AdminSerializer, InstructorSerializer, StudentSerializer

class SuperAdminViewSet(ModelViewSet):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer
    pagination_class = DefaultPagination

class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    pagination_class = DefaultPagination

class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    pagination_class = DefaultPagination

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = DefaultPagination