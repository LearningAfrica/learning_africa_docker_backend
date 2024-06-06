from django.contrib import admin
from .models import SuperAdmin, Admin, Instructor, Student

@admin.register(SuperAdmin)
class SuperAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_select_related = ['user']
    list_per_page = 20

@admin.register(Admin)
class Admin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_select_related = ['user']
    list_per_page = 20

@admin.register(Instructor)
class Instructor(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_select_related = ['user']
    list_per_page = 20

@admin.register(Student)
class Student(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_select_related = ['user']
    list_per_page = 20