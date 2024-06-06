from rest_framework import permissions
from system_users.models import Student
from courses.models import OrganizationInstructor, StudentCourseEnrollment

class IsSysAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_super_admin)
    
class IsOrgAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_admin)
    
class IsInstructor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_instructor)
    
class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_student)
    
class IsEnrolled(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        student_id = Student.objects.get(user_id=request.user.id)
        # return obj.students.filter(id=student_id).exists()
        return StudentCourseEnrollment.objects.filter(student=student_id).exists()
    
class OrganizationPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_super_admin:
            return True
        
        if user.is_admin:
            return request.query_params.get('admin_organization') == str(user.admin.organization.id)
        
        if user.is_instructor:
            return OrganizationPermission.objects.filter(
                instructor=user.instructor,
                organization_id=request.query_params.get('instructor_organization')
            ).exists()
            # return request.query_params.get('instructor_organization') == str(user.instructor.organization.id)
        
        return False