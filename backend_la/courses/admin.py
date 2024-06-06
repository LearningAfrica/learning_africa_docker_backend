from django.contrib import admin
from .models import (Category, Course, Module, 
                     Content, Organization, OrganizationAdmin, 
                     OrganizationInstructor, OrganizationStudent,
                     StudentCourseEnrollment)

@admin.register(Category)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(StudentCourseEnrollment)
admin.site.register(Organization)
admin.site.register(OrganizationAdmin)
admin.site.register(OrganizationInstructor)
admin.site.register(OrganizationStudent)
admin.site.register(Module)
admin.site.register(Content)