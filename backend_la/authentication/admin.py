from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 
                     'is_staff', 'is_superuser', 'is_active', 
                    'is_verified', 'is_super_admin', 'is_admin', 'is_instructor', 
                    'is_student']
    list_per_page = 20