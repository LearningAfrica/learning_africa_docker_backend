from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SuperAdmin, Admin, Instructor, Student

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_student(sender, instance, created, **kwargs):
    if created:
        if getattr(instance, 'is_super_admin', False):
            SuperAdmin.objects.create(user=instance)
        elif getattr(instance, 'is_admin', False):
            Admin.objects.create(user=instance)
        elif getattr(instance, 'is_instructor', False):
            Instructor.objects.create(user=instance)
        elif getattr(instance, 'is_student', False):
            Student.objects.create(user=instance)