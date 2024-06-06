from rest_framework import serializers
from .models import SuperAdmin, Admin, Instructor, Student

class SuperAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuperAdmin
        fields = ['first_name', 'last_name']

class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = ['first_name', 'last_name']

class InstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name']

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['first_name', 'last_name']