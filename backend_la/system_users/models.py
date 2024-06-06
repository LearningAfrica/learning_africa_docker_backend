from django.db import models
from django.contrib import admin
from django.conf import settings

class SuperAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username
    
    class Meta:
        db_table = 'sys_admins'
        verbose_name_plural = 'Super Admins'
        ordering = ['user__first_name', 'user__last_name']

class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username
    
    class Meta:
        db_table = 'admins'
        verbose_name_plural = 'Admins'
        ordering = ['user__first_name', 'user__last_name']

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='instructor_profile', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username
    
    class Meta:
        db_table = 'instructors'
        verbose_name_plural = 'Instructors'
        ordering = ['user__first_name', 'user__last_name']

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username
    
    class Meta:
        db_table = 'students'
        verbose_name_plural = 'Students'
        ordering = ['user__first_name', 'user__last_name']