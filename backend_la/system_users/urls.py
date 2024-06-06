from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('super_admins', views.SuperAdminViewSet, basename='super_admins')
router.register('admins', views.AdminViewSet, basename='admins')
router.register('instructors', views.InstructorViewSet, basename='instructors')
router.register('students', views.StudentViewSet, basename='students')

urlpatterns = router.urls