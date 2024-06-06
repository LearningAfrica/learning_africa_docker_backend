from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action

from utils.permissions import IsSysAdmin, IsInstructor, IsEnrolled, IsStudent, OrganizationPermission, IsOrgAdmin
from utils.pagination import DefaultPagination
from . import models
from . import serializers
from system_users.models import Student

class OrganizationViewSet(ModelViewSet):
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()
    permission_classes = [permissions.IsAuthenticated,]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOrgAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id,
        }

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrganizationAdminSerializer
        return serializers.OrganizationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return models.Organization.objects.all()
        elif user.is_admin:
            admin = models.Admin.objects.get(user__id=user.id)
            return models.Organization.objects.filter(organizationadmin__admin=admin)
        elif user.is_instructor:
            instructor = models.Instructor.objects.get(user=user)
            return models.Organization.objects.filter(organizationinstructor__instructor=instructor)
        elif user.is_student:
            student = models.Student.objects.get(user=user)
            return models.Organization.objects.filter(organizationstudent__student=student)
        else:
            return models.Organization.objects.none()

class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [IsInstructor()]

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id,
        }
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCategorySerializer
        return serializers.CategorySerializer
    
class InstructorOrgViewSet(ModelViewSet):
    http_method_names = ['get']
    
    serializer_class = serializers.InstructorOrgSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        instructor = models.Instructor.objects.get(user=self.request.user)
        return models.OrganizationInstructor.objects.filter(instructor=instructor).all()
    
class CourseStudentViewSet(ModelViewSet):
    http_method_names = ['get']

    permission_classes = [permissions.IsAuthenticated]
    
    serializer_class = serializers.CourseStudentSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('course_pk', None)
        user = self.request.user
        if user.is_student:
            return models.StudentCourseEnrollment.objects.none()
        
        if course_id:
            return models.StudentCourseEnrollment.objects.filter(course_id=self.kwargs['course_pk'])
        else:
            return models.StudentCourseEnrollment.objects.none()

class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.action == 'enroll':
            return [IsStudent()]
        elif self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [IsInstructor(),]
        
    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id,
        }
        
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCourseSerializer
        return serializers.CourseSerializer
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        student = Student.objects.get(user_id=request.user.id)
        if isinstance(student, Student):
            models.StudentCourseEnrollment.objects.create(course=course, student=student)
            return Response({'detail': 'Enrolled successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Enrolled failed. Not student'}, status=status.HTTP_403_FORBIDDEN)
        
    @action(detail=True, 
            methods=['get'],
            serializer_class=serializers.CourseWithContentSerializer)
            # permission_classes=[IsEnrolled])
    def contents(self, request, *args, **kwargs):
        course = self.get_object()
        student = Student.objects.get(user_id=request.user.id)
        if models.StudentCourseEnrollment.objects.filter(course=course, student=student).exists():
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({'detail': 'You are not enrolled in this course'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if request.user == instance.instructor.user:
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({'detail': 'Permission denied.You are not the owner of this course.'}, status=status.HTTP_403_FORBIDDEN)
    
class ModuleViewSet(ModelViewSet):
    queryset = models.Module.objects.all()
    serializer_class = serializers.ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [IsInstructor()]
    
    def get_queryset(self):
        course_id = self.kwargs.get('course_pk', '')
        if course_id:
            return models.Module.objects.filter(course_id=course_id)
        return models.Module.objects.all()
    
class ContentViewSet(ModelViewSet):

    queryset = models.Content.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [IsInstructor()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateContentSerializer
        return serializers.ContentSerializer
    
    def get_queryset(self):
        module_id = self.kwargs.get('module_pk', '')
        if module_id:
            return models.Content.objects.filter(module_id=module_id)
        return models.Content.objects.all()